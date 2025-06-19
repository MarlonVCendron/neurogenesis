import pickle
from skopt import gp_minimize, load
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt.callbacks import CheckpointSaver
import numpy as np
from brian2 import ms, second, Hz
from os.path import join
import os
import time
import copy

from sim import SimWrapper
from params.synapses import syn_params
from params.cells import cell_params
from utils.patterns import generate_activity_patterns
from params import results_dir, stim_time
from utils.args_config import args

# --- CONFIG ---
N_AVG_RUNS = 2 # Number of runs to average for a stable result
N_CALLS = 200  # Total number of parameter sets to test

# --- PATHS ---
results_path = join(results_dir, "fit_results")
os.makedirs(results_path, exist_ok=True)
checkpoint_path = join(results_path, "checkpoint.pkl")

# --- Globals for ETA tracking ---
start_time = time.time()
eval_count = 0

# --- PARAMETER SPACE ---
space = [
    Real(1e-3, 0.15, name='p_pp_mgc', prior='log-uniform'),
    Real(1e-3, 0.5, name='p_pp_mc', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_pp_bc', prior='log-uniform'),
    Real(1e-3, 0.5, name='p_pp_pca3', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_pp_ica3', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_mgc_mc', prior='log-uniform'),
    Real(1e-3, 0.2, name='p_mgc_pca3', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_mc_mgc', prior='log-uniform'),
    Real(1e-3, 0.6, name='p_pca3_pca3', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_pca3_mc', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_pca3_ica3', prior='log-uniform'),
    Real(1e-3, 1.0, name='p_ica3_pca3', prior='log-uniform'),
    Integer(10, 20, name='active_p_perc'),
    Integer(20, 60, name='pp_hz')
]

# --- OBJECTIVE FUNCTION ---
@use_named_args(space)
def evaluate_network(**params):
    global eval_count, start_time
    eval_start_time = time.time()

    # Build syn_params override dictionary from the provided parameters
    syn_params_override = copy.deepcopy(syn_params)
    for key, value in params.items():
        if key.startswith('p_'):
            syn_name = key.replace('p_', '')
            if syn_name in syn_params_override:
                syn_params_override[syn_name]['p'] = value

                # If it's an MGC synapse, also apply to IGC if it exists
                if 'mgc' in syn_name:
                    igc_syn_name = syn_name.replace('mgc', 'igc')
                    if igc_syn_name in syn_params_override:
                        syn_params_override[igc_syn_name]['p'] = value

    # Generate a set of input patterns for this evaluation
    active_p = params['active_p_perc'] / 100.0
    pp_hz = params['pp_hz'] * Hz
    patterns = generate_activity_patterns(active_p=active_p, pp_hz=pp_hz)
    
    # Store metrics for both neurogenesis and control conditions
    all_metrics = {'neurogenesis': [], 'control': []}

    original_no_neurogenesis = args.no_neurogenesis
    # for condition in ['neurogenesis', 'control']:
    for condition in ['neurogenesis']:
        # Set the appropriate global flag for the simulation
        args.no_neurogenesis = (condition == 'control')
        
        for i in range(N_AVG_RUNS):
            print(f"Running {condition}, run {i+1}/{N_AVG_RUNS} with params: {params}")
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
    # avg_sparsity_control = {name: np.mean([m['sparsity'].get(name, 0) for m in all_metrics['control']]) for name in cell_params}
    
    print("\n--- Averaged Results ---")
    print("Neurogenesis Rates (Hz):", {k: f"{v:.2f}" for k, v in avg_rates_ng.items() if v > 0})
    # print("MGC Sparsity (Control):", f"{avg_sparsity_control.get('mgc', 0):.2%}")
    print("------------------------\n")

    # --- Calculate Combined Cost ---
    cost = 0.0
    
    # Target rates for neurogenesis (very important)
    cost += ((avg_rates_ng.get('mgc', 0)*Hz - 0.4*Hz)/(0.4*Hz))**2 * 5
    cost += ((avg_rates_ng.get('igc', 0)*Hz - 2.4*Hz)/(2.4*Hz))**2 * 5
    
    # Target rates (less important)
    cost += ((avg_rates_ng.get('mc', 0)*Hz - 1.0*Hz)/(1.0*Hz))**2 * 2
    
    # High rates for bc and ica3
    if avg_rates_ng.get('bc', 0) < 20.0: cost += (20.0 - avg_rates_ng.get('bc', 0)) * 2
    if avg_rates_ng.get('hipp', 0) < 20.0: cost += (20.0 - avg_rates_ng.get('hipp', 0)) * 2
    if avg_rates_ng.get('ica3', 0) < 20.0: cost += (20.0 - avg_rates_ng.get('ica3', 0)) * 2
        
    # Sparsity for pca3 (neurogenesis)
    pca3_sparsity = avg_sparsity_ng.get('pca3', 0)
    if not (0.05 <= pca3_sparsity <= 0.9):
        cost += min(abs(pca3_sparsity - 0.05), abs(pca3_sparsity - 0.9)) * 30

    # Sparsity for mgc (control)
    mgc_sparsity = avg_sparsity_ng.get('mgc', 0)
    if not (0.05 <= mgc_sparsity <= 0.9):
        cost += min(abs(mgc_sparsity - 0.05), abs(mgc_sparsity - 0.9)) * 30

    # Penalize silent populations in neurogenesis condition
    for name in ['mgc', 'igc', 'mc', 'bc', 'hipp', 'pca3', 'ica3']:
        if avg_rates_ng.get(name, 0) < 0.01: # Check for near-silent instead of exactly 0
            cost += 1000

    print(f"Total Cost for this set of parameters: {cost:.4f}")
    
    # --- ETA Calculation ---
    eval_count += 1
    eval_time = time.time() - eval_start_time
    total_elapsed = time.time() - start_time
    avg_time_per_eval = total_elapsed / eval_count
    remaining_evals = N_CALLS - eval_count
    eta_seconds = avg_time_per_eval * remaining_evals
    
    print(f"--- Evaluation {eval_count}/{N_CALLS} finished in {eval_time:.2f}s ---")
    print(f"--- Estimated time remaining: {eta_seconds/3600:.2f} hours ---")

    return cost

# --- OPTIMIZATION ---
if __name__ == "__main__":
    checkpoint_saver = CheckpointSaver(checkpoint_path, compress=9)

    try:
        res_gp = load(checkpoint_path)
        x0 = res_gp.x_iters
        y0 = res_gp.func_vals

        best_idx = np.argmin(res_gp.func_vals)
        best_x = res_gp.x_iters[best_idx]
        best_score = res_gp.func_vals[best_idx]
        
        # print("\nBest result from checkpoint:")
        # print("Best parameters found:", {space[i].name: best_x[i] for i in range(len(space))})
        # print("Best score (cost):", best_score)
        # exit()
        
        print("Resuming optimization from checkpoint.")
    except (FileNotFoundError, EOFError, IndexError):
        res_gp = None
        x0 = None
        y0 = None
        print("Starting new optimization.")

    result = gp_minimize(
        evaluate_network,
        space,
        x0=x0,
        y0=y0,
        n_calls=N_CALLS,
        n_initial_points=10,
        random_state=42,
        verbose=True,
        callback=[checkpoint_saver]
    )

    print("\nOptimization finished.")
    print("Best parameters found: ", {space[i].name: result.x[i] for i in range(len(space))})
    print("Best score (cost): ", result.fun)

    # You can now take the best parameters from result.x and use them
    # in your standard simulation, including running with the --no-neurogenesis flag
    # to check for the MGC sparsity in that condition.
