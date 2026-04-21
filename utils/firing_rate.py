import numpy as np
from brian2 import Hz, ms
from params import break_time

SMOOTH_WIDTH = 50 * ms

def get_population_firing_rates(rate_monitor):
    if rate_monitor is None:
        return np.zeros(0)
    mask = rate_monitor.t > break_time
    return rate_monitor.smooth_rate(window='flat', width=SMOOTH_WIDTH)[mask] / Hz
