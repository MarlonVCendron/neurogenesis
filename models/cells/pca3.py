from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Pyramidal CA3 cell
def create_pca3(N=None):
  params = cell_params['pca3'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  pca3 = create_neuron_group(**params)
  return pca3
