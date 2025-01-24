from brian2 import *
from neurogenesis.utils.create_neuron_group import create_neuron_group
from neurogenesis.params import cell_params

# Basket cell
def create_bc(N=None):
  params = cell_params['bc'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  bc = create_neuron_group(**params)
  return bc
