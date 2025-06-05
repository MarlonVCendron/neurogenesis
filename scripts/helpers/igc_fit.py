# Not made by me

import numpy as np
from scipy.optimize import minimize

# Known parameters (mV, ms, pA, pF, nS)
Vr_val = -63.2  # Resting potential (mV)
# Vt_val = -43.2  # Threshold potential (mV) - Will be fit
# Vreset_val = -48.2 # Reset potential (mV) - Will be fit
Vpeak_val = 83.5  # Spike peak (mV)
Cm_val = 24.6  # Membrane capacitance (pF)

# Simulation time step
DT = 0.1  # ms


def izhikevich_simulation(params, I_ext_val, t_sim_ms):
    """
    Simulates a simple Izhikevich neuron.

    Args:
        params (tuple): (k, a, b, d, V_reset, V_threshold) neuron parameters.
                        k: pA/mV^2
                        a: 1/ms
                        b: nS (pA/mV)
                        d: pA
                        V_reset: mV
                        V_threshold: mV
        I_ext_val (float): External current (pA).
        t_sim_ms (float): Total simulation time (ms).

    Returns:
        list: Spike times (ms).
    """
    k_param, a_param, b_param, d_param, v_reset_param, v_thresh_param = params

    num_steps = int(t_sim_ms / DT)
    v_trace = np.zeros(num_steps)
    u_trace = np.zeros(num_steps)
    spike_times = []

    # Initial conditions
    v = Vr_val
    u = 0.0  # Typically u is initialized to 0 or b_param * (Vr_val - Vr_val)

    for i in range(num_steps):
        v_trace[i] = v
        u_trace[i] = u

        if v >= Vpeak_val:
            v = v_reset_param
            u = u + d_param
            spike_times.append(i * DT)

        # Euler integration step
        dv_dt = (k_param * (v - Vr_val) * (v - v_thresh_param) - u + I_ext_val) / Cm_val
        du_dt = a_param * (b_param * (v - Vr_val) - u)

        v = v + dv_dt * DT
        u = u + du_dt * DT

    return spike_times


def objective_function(params_tuple):
    """
    Objective function to minimize.
    Calculates error based on target spiking behaviors.
    """
    # Ensure parameters are positive where necessary (handled by bounds in minimize, but good for direct calls)
    # k_param > 0, a_param > 0 generally. d_param usually > 0. b_param can sometimes be negative.
    # For this problem, we can expect them to be mostly positive based on typical Izhikevich cells.

    if not all(isinstance(p, (int, float)) for p in params_tuple):
        print(f"Invalid parameter types received: {params_tuple}")
        return 1e12

    current_k, current_a, current_b, current_d, current_v_reset, current_v_thresh = params_tuple

    if current_k <= 0 or current_a <= 0:
        print(
            f"Objective call with non-positive k or a: k={current_k:.4f}, a={current_a:.4f}, b={current_b:.4f}, d={current_d:.4f}, Vreset={current_v_reset:.2f}, Vthresh={current_v_thresh:.2f} -> High penalty"
        )
        return 1e12

    error = 0.0

    # Condition 1: 20pA, 500ms, 1 spike @ ~140ms
    I1, T1, target_spikes1, target_first_spike_ms1 = 20.0, 500.0, 1, 140.0
    spikes_t1 = izhikevich_simulation(params_tuple, I1, T1)
    num_spikes1 = len(spikes_t1)

    error += (num_spikes1 - target_spikes1) ** 2 * 100

    if num_spikes1 > 0:
        first_spike_ms1 = spikes_t1[0]
        error += ((first_spike_ms1 - target_first_spike_ms1) / 10.0)**2 # Scaled error for first spike time
    elif target_spikes1 > 0 : # No spike, but one was expected
        error += ((T1 - target_first_spike_ms1) / 10.0)**2 # Penalize based on how far off the end of sim is

    # Condition 2: 40pA, 500ms, spikes at ~80, ~190, ~270, ~330, ~380 ms
    I2, T2 = 40.0, 500.0
    target_spike_times_c2 = [80.0, 190.0, 270.0, 330.0, 380.0]
    target_num_spikes_c2 = len(target_spike_times_c2)

    spikes_t2 = izhikevich_simulation(params_tuple, I2, T2)
    num_spikes2 = len(spikes_t2)

    error += (num_spikes2 - target_num_spikes_c2) ** 2

    # # error += timing_error_c2 # User commented this out, consistent with ISI focus
    # Add penalty for ISI variability if there are enough spikes
    if num_spikes2 >= 2:
        isis_c2 = np.diff(spikes_t2)
        std_isi_c2 = np.std(isis_c2)
        error += (std_isi_c2 / 10.0)**2 # Penalize deviation from regular spiking (target std_dev = 0)
    elif num_spikes2 == 1 and target_num_spikes_c2 > 1: # Only one spike when more were expected
        # Spike count error already covers this, but could add a fixed penalty for inability to check ISI
        error += ((target_num_spikes_c2 - 1) * (50.0/10.0)**2) # Arbitrary penalty for missing ISIs (e.g. 50ms deviation per missing ISI)

    # Condition 3: 60pA, 500ms, 10 spikes
    I3, T3, target_spikes3 = 60.0, 500.0, 10
    spikes_t3 = izhikevich_simulation(params_tuple, I3, T3)
    num_spikes3 = len(spikes_t3)
    error += (num_spikes3 - target_spikes3) ** 2

    # Condition 4: 80pA, 500ms, 16 spikes
    I4, T4, target_spikes4 = 80.0, 500.0, 16
    spikes_t4 = izhikevich_simulation(params_tuple, I4, T4)
    num_spikes4 = len(spikes_t4)
    error += (num_spikes4 - target_spikes4) ** 2

    print(
        f"Params: k={params_tuple[0]:.4f}, a={params_tuple[1]:.4f}, b={params_tuple[2]:.4f}, d={params_tuple[3]:.4f}, Vrst={params_tuple[4]:.2f}, Vthr={params_tuple[5]:.2f} | Error: {error:.4f}"
    )
    return error


if __name__ == "__main__":
    # Initial guess for parameters (k, a, b, d, V_reset, V_threshold)
    # k: pA/mV^2, a: 1/ms, b: nS (pA/mV), d: pA, V_reset: mV, V_threshold: mV
    initial_params = [0.1, 0.003, -5.0, 10.0, -48.2, -43.2]

    # Bounds for parameters
    bounds = [
        (0.01, 10.0),  # k_param (pA/mV^2)
        (0.001, 0.5),  # a_param (1/ms)
        (-50.0, 50.0),  # b_param (nS or pA/mV)
        (0.0, 100.0),  # d_param (pA)
        (-80.0, -35.0),  # V_reset (mV)
        (-55.0, -25.0),  # V_threshold (mV)
    ]

    print("Starting optimization with 6 parameters (k, a, b, d, V_reset, V_thresh)...")
    result = minimize(
        objective_function,
        initial_params,
        method="Nelder-Mead",
        bounds=bounds, 
        options={
            "disp": True,
            "maxiter": 3000,
            "xatol": 1e-9,
            "fatol": 1e-9,
        },
    )

    if result.success:
        fitted_params = result.x
        print("\nOptimization successful.")
        print(f"Fitted parameters (k, a, b, d, V_reset, V_threshold):")
        print(f"  k = {fitted_params[0]:.4f} pA/mV^2")
        print(f"  a = {fitted_params[1]:.4f} 1/ms")
        print(f"  b = {fitted_params[2]:.4f} nS (pA/mV)")
        print(f"  d = {fitted_params[3]:.4f} pA")
        print(f"  V_reset = {fitted_params[4]:.2f} mV")
        print(f"  V_threshold = {fitted_params[5]:.2f} mV")
        print(f"Final objective function value: {result.fun:.4f}")

        # Optional: Verify with the fitted parameters
        print("\nVerifying with fitted parameters:")
        # k_fit, a_fit, b_fit, d_fit = fitted_params # Unpacking all 6 is better

        # Condition 1
        spikes_c1 = izhikevich_simulation(fitted_params, 20.0, 500.0)
        first_spike_c1 = spikes_c1[0] if spikes_c1 else -1
        print(
            f"Cond 1 (20pA, 500ms, Tgt: 1 spk @ ~140ms): {len(spikes_c1)} spikes. First at {first_spike_c1:.2f} ms"
        )

        # Condition 2
        spikes_c2 = izhikevich_simulation(fitted_params, 40.0, 500.0)
        target_s_c2_count = 5 # Target count for C2
        print_spikes_c2 = [f'{s:.1f}' for s in spikes_c2]
        isis_c2_verify = []
        std_isi_c2_verify = -1.0
        if len(spikes_c2) >= 2:
            isis_c2_verify = np.diff(spikes_c2)
            std_isi_c2_verify = np.std(isis_c2_verify)
        
        print(
            f"Cond 2 (40pA, 500ms, Tgt: {target_s_c2_count} reg. spk): {len(spikes_c2)} spikes. Times: {print_spikes_c2}. ISIs: {[f'{i:.1f}' for i in isis_c2_verify]}. ISI StdDev: {std_isi_c2_verify:.2f}"
        )

        # Condition 3
        spikes_c3 = izhikevich_simulation(fitted_params, 60.0, 500.0)
        print(f"Cond 3 (60pA, 500ms, Tgt: 10 spk): {len(spikes_c3)} spikes")

        # Condition 4
        spikes_c4 = izhikevich_simulation(fitted_params, 80.0, 500.0)
        print(f"Cond 4 (80pA, 500ms, Tgt: 16 spk): {len(spikes_c4)} spikes")

    else:
        print("\nOptimization failed.")
        print(result.message)
