from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Mossy cell
def create_mc(N=None):
  params = cell_params['mc'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  mc = create_neuron_group(**params)
  return mc
