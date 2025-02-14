from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Mature granule cell
def create_mgc(N=None):
  params = cell_params['mgc'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  mgc = create_neuron_group(**params)
  return mgc
