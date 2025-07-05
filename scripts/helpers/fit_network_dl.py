import os
import time
import copy
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from brian2 import ms, second, Hz

from sim import SimWrapper
from params.synapses import syn_params
from params.cells import cell_params
from utils.patterns import generate_activity_patterns
from params import results_dir, stim_time
from utils.args_config import args

# --- CONFIG ---
N_INITIAL_SAMPLES = 40  # Number of random samples to start with
N_ITERATIONS = 20      # Number of optimization iterations
N_CANDIDATES_PER_ITER = 3 # Number of new candidates to evaluate per iteration
N_AVG_RUNS = 2          # Number of runs to average for a stable result
N_EPOCHS = 200           # Training epochs for the surrogate model
N_ENSEMBLE = 5          # Number of models in the surrogate ensemble
ACQUISITION_KAPPA = 2.5 # Kappa for LCB acquisition function

# --- PATHS ---
results_path = os.path.join(results_dir, "fit_results_dl")
os.makedirs(results_path, exist_ok=True)
data_path = os.path.join(results_path, "optimization_data.pkl")

# --- Globals for ETA tracking ---
start_time = time.time()
total_evals = 0

# --- PARAMETER SPACE DEFINITION ---
# Expanded parameter space for more detailed tuning
param_space = {
    'p_pp_mgc': (1e-3, 0.15),
    'p_pp_mc': (1e-3, 0.5),
    'p_pp_bc': (1e-3, 1.0),
    'p_pp_pca3': (1e-3, 0.5),
    'p_pp_ica3': (1e-3, 1.0),
    'p_mgc_mc': (1e-3, 1.0),
    'p_mgc_pca3': (1e-3, 0.2),
    'p_mgc_hipp': (1e-3, 0.5),
    'p_mgc_bc': (1e-3, 1.0),
    'p_mc_mgc': (1e-3, 1.0),
    'p_mc_hipp': (1e-3, 1.0),
    'p_mc_bc': (1e-3, 1.0),
    'p_pca3_pca3': (1e-3, 0.6),
    'p_pca3_mc': (1e-3, 1.0),
    'p_pca3_ica3': (1e-3, 1.0),
    'p_ica3_pca3': (1e-3, 1.0),
    'p_hipp_mgc': (1e-3, 0.5),
    'p_hipp_bc': (1e-3, 0.1),
    'p_bc_mgc': (1e-3, 1.0),
    'p_bc_hipp': (1e-3, 0.1),
    'active_p_perc': (10, 20),
    'pp_hz': (20, 60)
}
param_names = list(param_space.keys())

# --- SURROGATE MODEL (MLP) ---
class SurrogateModel(nn.Module):
    def __init__(self, n_params):
        super(SurrogateModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(n_params, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    def forward(self, x):
        return self.network(x)

# --- HELPER FUNCTIONS ---
def sample_params():
    """Sample a random set of parameters from the defined space."""
    params = {}
    for name, (low, high) in param_space.items():
        # Using log uniform for 'p_' params
        if name.startswith('p_'):
            params[name] = np.exp(np.random.uniform(np.log(low), np.log(high)))
        else: # Uniform for integer params
            params[name] = np.random.uniform(low, high)
            if 'perc' in name or 'hz' in name:
                params[name] = int(params[name])
    return params

def normalize_params(params_list):
    """Normalize parameters to [0, 1] for the network."""
    normalized = []
    for params in params_list:
        norm_p = []
        for name in param_names:
            val = params[name]
            low, high = param_space[name]
            if name.startswith('p_'): # Log scale normalization
                norm_p.append((np.log(val) - np.log(low)) / (np.log(high) - np.log(low)))
            else: # Linear scale
                norm_p.append((val - low) / (high - low))
        normalized.append(norm_p)
    return torch.FloatTensor(normalized)

def denormalize_params(norm_params_tensor):
    """Denormalize parameters from [0, 1] back to their original space."""
    denormalized = []
    norm_params_list = norm_params_tensor.cpu().numpy()
    for norm_p in norm_params_list:
        params = {}
        for i, name in enumerate(param_names):
            val = norm_p[i]
            low, high = param_space[name]
            if name.startswith('p_'):
                params[name] = np.exp(val * (np.log(high) - np.log(low)) + np.log(low))
            else:
                raw_val = val * (high - low) + low
                if 'perc' in name or 'hz' in name:
                    params[name] = int(raw_val)
                else:
                    params[name] = raw_val
        denormalized.append(params)
    return denormalized

# --- OBJECTIVE FUNCTION ---
def evaluate_network(params):
    """Runs the simulation and computes the cost for a given parameter set."""
    global total_evals, start_time
    eval_start_time = time.time()

    syn_params_override = copy.deepcopy(syn_params)
    for key, value in params.items():
        if key.startswith('p_'):
            syn_name = key.replace('p_', '')
            if syn_name in syn_params_override:
                syn_params_override[syn_name]['p'] = value
                if 'mgc' in syn_name:
                    igc_syn_name = syn_name.replace('mgc', 'igc')
                    if igc_syn_name in syn_params_override:
                        syn_params_override[igc_syn_name]['p'] = value

    active_p = params['active_p_perc'] / 100.0
    pp_hz = params['pp_hz'] * Hz
    patterns = generate_activity_patterns(active_p=active_p, pp_hz=pp_hz)

    # Store metrics for both neurogenesis and control conditions
    all_metrics = {'neurogenesis': [], 'control': []}

    original_no_neurogenesis = args.no_neurogenesis
    for condition in ['neurogenesis', 'control']:
        # Set the appropriate global flag for the simulation
        args.no_neurogenesis = (condition == 'control')
        
        for i in range(N_AVG_RUNS):
            print(f"Running {condition}, run {i+1}/{N_AVG_RUNS} for params: { {k: f'{v:.4f}' if isinstance(v, float) else v for k, v in params.items()} }")
            sim = SimWrapper(syn_params_arg=syn_params_override, monitor_rate=False, report='text')
            
            # Use a different pattern for each avg run to get a better sample
            pattern_dict = patterns[i % len(patterns)]
            
            spikes_list, _, _ = sim.do_run(pattern_dict, results_directory=None, save=False)
            spikes = {mon.source.name: mon for mon in spikes_list}

            # Calculate and store metrics for this run
            duration_s = stim_time / second
            run_rates = {name: mon.num_spikes / (cell_params[name]['N'] * duration_s) for name, mon in spikes.items()}
            run_sparsity = {name: len(np.unique(mon.i)) / cell_params[name]['N'] for name, mon in spikes.items() if cell_params[name]['N'] > 0}
            all_metrics[condition].append({'rates': run_rates, 'sparsity': run_sparsity})

    args.no_neurogenesis = original_no_neurogenesis # Reset global flag

    # --- Average the metrics from all runs ---
    avg_rates_ng = {name: np.mean([m['rates'].get(name, 0) for m in all_metrics['neurogenesis']]) for name in cell_params}
    avg_sparsity_ng = {name: np.mean([m['sparsity'].get(name, 0) for m in all_metrics['neurogenesis']]) for name in cell_params}
    avg_rates_control = {name: np.mean([m['rates'].get(name, 0) for m in all_metrics['control']]) for name in cell_params}
    avg_sparsity_control = {name: np.mean([m['sparsity'].get(name, 0) for m in all_metrics['control']]) for name in cell_params}
    
    print("\n--- Averaged Results (Neurogenesis) ---")
    print("Rates (Hz):", {k: f"{v:.2f}" for k, v in avg_rates_ng.items() if v > 0})
    print("Sparsity:", {k: f"{v:.2%}" for k, v in avg_sparsity_ng.items() if v > 0})
    print("\n--- Averaged Results (Control) ---")
    print("Rates (Hz):", {k: f"{v:.2f}" for k, v in avg_rates_control.items() if v > 0})
    print("Sparsity:", {k: f"{v:.2%}" for k, v in avg_sparsity_control.items() if v > 0})
    print("------------------------\n")

    # --- Refined Cost Function ---
    cost = 0.0
    
    # === Cost from Neurogenesis condition ===
    # Sparsity goals: prefer 5-10%, but closer to 5% is better
    for pop in ['mgc', 'pca3']:
        sparsity = avg_sparsity_ng.get(pop, 0)
        # Strong penalty for being too sparse (below 5%)
        if sparsity < 0.05:
            cost += ((sparsity - 0.05)**2) * 200
        # Medium penalty for being too dense (above 10%)
        elif sparsity > 0.1:
            cost += ((sparsity - 0.1)**2) * 100
        # Gentle push towards 5% within the [5%, 10%] range
        else:
            cost += ((sparsity - 0.05)**2) * 200 # Gently push towards 5%
    
    # Firing rate goals for excitatory cells (low but active)
    cost += ((avg_rates_ng.get('mgc', 0) - 0.5)**2) * 10
    cost += ((avg_rates_ng.get('igc', 0) - 2.5)**2) * 10
    cost += ((avg_rates_ng.get('pca3', 0) - 1.0)**2) * 10
    cost += ((avg_rates_ng.get('mc', 0) - 2.0)**2) * 5

    # Encourage interneuron activity
    for inh_pop in ['bc', 'hipp', 'ica3']:
        rate = avg_rates_ng.get(inh_pop, 0)
        if rate < 15.0:
            cost += ((15.0 - rate)**2) * 0.2

    # Ensure MGC/PCA3 rates are lower than interneurons
    avg_inh_rate_ng = np.mean([avg_rates_ng.get(p, 0) for p in ['bc', 'hipp', 'ica3']])
    
    mgc_rate_ng = avg_rates_ng.get('mgc', 0)
    if mgc_rate_ng > avg_inh_rate_ng: 
        cost += (mgc_rate_ng - avg_inh_rate_ng)**2 * 5
        
    pca3_rate_ng = avg_rates_ng.get('pca3', 0)
    if pca3_rate_ng > avg_inh_rate_ng: 
        cost += (pca3_rate_ng - avg_inh_rate_ng)**2 * 5

    # Penalize silent populations heavily in neurogenesis
    min_rate_penalty = 0.05 # Hz
    for name in ['mgc', 'igc', 'mc', 'bc', 'hipp', 'pca3', 'ica3']:
        rate = avg_rates_ng.get(name, 0)
        if rate < min_rate_penalty:
            cost += ((min_rate_penalty - rate)**2) * 50000

    # === Cost from Control (no neurogenesis) condition ===
    # 1. MGC sparsity should remain in a healthy range (5-15%)
    mgc_sparsity_ctrl = avg_sparsity_control.get('mgc', 0)
    if not (0.05 <= mgc_sparsity_ctrl <= 0.15):
        cost += ((mgc_sparsity_ctrl - 0.1)**2) * 150 # Target 10%, penalize outside range

    # 2. Key populations should remain reasonably active
    if avg_rates_control.get('mc', 0) < 1.0:
        cost += (1.0 - avg_rates_control.get('mc', 0))**2 * 10
        
    for inh_pop in ['bc', 'hipp', 'ica3']:
        if avg_rates_control.get(inh_pop, 0) < 10.0:
            cost += (10.0 - avg_rates_control.get(inh_pop, 0))**2 * 3
            
    # 3. Penalize silent populations heavily in control (excluding IGCs)
    for name in ['mgc', 'mc', 'bc', 'hipp', 'ica3']:
        rate = avg_rates_control.get(name, 0)
        if rate < min_rate_penalty:
            cost += ((min_rate_penalty - rate)**2) * 50000


    print(f"Total Cost for this set of parameters: {cost:.4f}")
    
    # --- ETA Calculation ---
    total_evals += 1
    eval_time = time.time() - eval_start_time
    total_elapsed = time.time() - start_time
    avg_time_per_eval = total_elapsed / total_evals
    
    print(f"--- Evaluation {total_evals} finished in {eval_time:.2f}s ---")
    print(f"--- Average time per evaluation: {avg_time_per_eval:.2f}s ---")

    metrics = {
        'neurogenesis': {'rates': avg_rates_ng, 'sparsity': avg_sparsity_ng},
        'control': {'rates': avg_rates_control, 'sparsity': avg_sparsity_control}
    }

    return cost, metrics

# --- main optimization loop ---
if __name__ == "__main__":
    # check for gpu
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"using device: {device}")

    # load existing data or initialize
    try:
        with open(data_path, 'rb') as f:
            optimization_history = pickle.load(f)
        
        
        print(f"resuming optimization from {len(optimization_history)} existing data points.")

        if optimization_history:
            evaluated_costs = [item['cost'] for item in optimization_history]
            best_idx = np.argmin(evaluated_costs)
            best_run = optimization_history[best_idx]
            
            print("\n--- Best Result So Far ---")
            print(f"Best Cost: {best_run['cost']:.4f}")
            print("Best Parameters:", {k: f'{v:.4f}' if isinstance(v, float) else v for k, v in best_run['params'].items()})
            print("---------------------------\n")
            
    except (FileNotFoundError, EOFError, IndexError):
        optimization_history = []
        print("starting new optimization: generating initial random samples...")
        for i in range(N_INITIAL_SAMPLES):
            print(f"--- initial sample {i+1}/{N_INITIAL_SAMPLES} ---")
            params = sample_params()
            cost, metrics = evaluate_network(params)
            optimization_history.append({'params': params, 'cost': cost, 'metrics': metrics})
            # save after each evaluation
            with open(data_path, 'wb') as f:
                pickle.dump(optimization_history, f)

    # optimization loop
    for it in range(N_ITERATIONS):
        print(f"\n--- starting optimization iteration {it+1}/{N_ITERATIONS} ---")
        
        # 1. train the surrogate model ensemble
        print("training surrogate model ensemble...")
        evaluated_params = [item['params'] for item in optimization_history]
        evaluated_costs_raw = torch.FloatTensor([item['cost'] for item in optimization_history]).view(-1, 1)

        # Normalize costs for stable training
        cost_mean = torch.mean(evaluated_costs_raw)
        cost_std = torch.std(evaluated_costs_raw)
        if cost_std < 1e-6: cost_std = torch.tensor(1.0) # Avoid division by zero if all costs are the same
        evaluated_costs = (evaluated_costs_raw - cost_mean) / cost_std
        evaluated_costs = evaluated_costs.to(device)
        
        X_normalized = normalize_params(evaluated_params).to(device)
        
        models = [SurrogateModel(X_normalized.shape[1]).to(device) for _ in range(N_ENSEMBLE)]
        for i, model in enumerate(models):
            print(f"Training model {i+1}/{N_ENSEMBLE}...")
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            criterion = nn.MSELoss()
            
            # Simple train/validation split for each model to prevent gross overfitting
            dataset = torch.utils.data.TensorDataset(X_normalized, evaluated_costs)
            train_size = int(0.9 * len(dataset))
            val_size = len(dataset) - train_size
            train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
            
            train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)
            val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=val_size)

            for epoch in range(N_EPOCHS):
                model.train()
                for x_batch, y_batch in train_loader:
                    optimizer.zero_grad()
                    outputs = model(x_batch)
                    loss = criterion(outputs, y_batch)
                    loss.backward()
                    optimizer.step()
                
                # Validation loss
                if (epoch + 1) % 40 == 0:
                    model.eval()
                    with torch.no_grad():
                        for x_val, y_val in val_loader:
                            val_outputs = model(x_val)
                            val_loss = criterion(val_outputs, y_val)
                    print(f"Epoch [{epoch+1}/{N_EPOCHS}], Train Loss: {loss.item():.4f}, Val Loss: {val_loss.item():.4f}")


        # 2. Propose new candidates using the model ensemble (LCB)
        print("Generating and evaluating new candidate parameters using LCB...")
        with torch.no_grad():
            # Generate a large number of random candidates
            candidate_param_dicts = [sample_params() for _ in range(2000)]
            candidate_params_norm = normalize_params(candidate_param_dicts).to(device)
            
            # Predict normalized costs with each model in the ensemble
            predictions_norm = torch.stack([model(candidate_params_norm) for model in models])
            
            # De-normalize predictions to calculate LCB on the original cost scale
            # Move cost stats to the correct device before using them
            cost_mean_dev = cost_mean.to(device)
            cost_std_dev = cost_std.to(device)

            mean_preds_norm = torch.mean(predictions_norm, axis=0)
            std_preds_norm = torch.std(predictions_norm, axis=0)

            mean_preds = (mean_preds_norm * cost_std_dev) + cost_mean_dev
            std_preds = std_preds_norm * cost_std_dev # Std dev only scales

            # Lower Confidence Bound (LCB) acquisition function
            lcb = mean_preds - ACQUISITION_KAPPA * std_preds
            
            # Select the top N candidates with the lowest LCB
            sorted_indices = torch.argsort(lcb.squeeze())
            best_candidate_indices = sorted_indices[:N_CANDIDATES_PER_ITER]
            
            new_params_to_eval = [candidate_param_dicts[i] for i in best_candidate_indices]

        # 3. Evaluate the new candidates with the real simulation
        print(f"Running simulation for {len(new_params_to_eval)} new best candidates...")
        for i, params in enumerate(new_params_to_eval):
            print(f"--- Candidate {i+1}/{len(new_params_to_eval)} from Iteration {it+1} ---")
            cost, metrics = evaluate_network(params)
            optimization_history.append({'params': params, 'cost': cost, 'metrics': metrics})
            # Save after each evaluation for robust checkpointing
            with open(data_path, 'wb') as f:
                pickle.dump(optimization_history, f)
                print("Saved optimization progress.")

        # Print current best result with detailed metrics
        evaluated_costs = [item['cost'] for item in optimization_history]
        best_idx = np.argmin(evaluated_costs)
        best_run = optimization_history[best_idx]
        
        print("\n--- Current Best Result ---")
        print(f"Best Cost: {best_run['cost']:.4f}")
        print("Best Parameters:", {k: f'{v:.4f}' if isinstance(v, float) else v for k, v in best_run['params'].items()})
        print("\n--- Metrics for Best Run ---")
        print("Neurogenesis:")
        print("  Rates (Hz):", {k: f"{v:.2f}" for k, v in best_run['metrics']['neurogenesis']['rates'].items() if v > 0})
        print("  Sparsity:", {k: f"{v:.2%}" for k, v in best_run['metrics']['neurogenesis']['sparsity'].items() if v > 0})
        print("Control:")
        print("  Rates (Hz):", {k: f"{v:.2f}" for k, v in best_run['metrics']['control']['rates'].items() if v > 0})
        print("  Sparsity:", {k: f"{v:.2%}" for k, v in best_run['metrics']['control']['sparsity'].items() if v > 0})
        print("---------------------------\n")

    print("\n--- Optimization Finished ---")
    evaluated_costs = [item['cost'] for item in optimization_history]
    best_idx = np.argmin(evaluated_costs)
    best_run = optimization_history[best_idx]
    print(f"Final Best Cost: {best_run['cost']:.4f}")
    print("Final Best Parameters:", best_run['params'])
    print("\n--- Final Metrics for Best Run ---")
    print("Neurogenesis:")
    print("  Rates (Hz):", {k: f"{v:.2f}" for k, v in best_run['metrics']['neurogenesis']['rates'].items() if v > 0})
    print("  Sparsity:", {k: f"{v:.2%}" for k, v in best_run['metrics']['neurogenesis']['sparsity'].items() if v > 0})
    print("Control:")
    print("  Rates (Hz):", {k: f"{v:.2f}" for k, v in best_run['metrics']['control']['rates'].items() if v > 0})
    print("  Sparsity:", {k: f"{v:.2%}" for k, v in best_run['metrics']['control']['sparsity'].items() if v > 0})
    print("---------------------------\n") 