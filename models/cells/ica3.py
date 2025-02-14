from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Inhibitory CA3 cell
def create_ica3(N=None):
  params = cell_params['ica3'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  ica3 = create_neuron_group(**params)
  return ica3
