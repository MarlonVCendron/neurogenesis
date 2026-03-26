from brian2 import second
from utils.patterns import get_population_spike_counts
from params import stim_time
import numpy as np

def get_population_firing_rates(monitor):
  if not monitor:
    return np.zeros(0, dtype=int)

  spike_counts = get_population_spike_counts(monitor)
  rates_hz = spike_counts / (stim_time / second)
  return rates_hz

