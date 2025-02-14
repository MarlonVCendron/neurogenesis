from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Hilar perforant path-associated cell
def create_hipp(N=None):
  params = cell_params['hipp'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  hipp = create_neuron_group(**params)
  return hipp
