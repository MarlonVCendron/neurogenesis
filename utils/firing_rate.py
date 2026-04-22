import numpy as np
from brian2 import second
from params import break_time, stim_time
from utils.patterns import get_population_spike_counts

def get_population_firing_rates(spike_monitor, t_start=break_time, t_end=None):
    if spike_monitor is None:
        return np.zeros(0)
    return get_population_spike_counts(spike_monitor, t_start=t_start, t_end=t_end) / (stim_time / second)
