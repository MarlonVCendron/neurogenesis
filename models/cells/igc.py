from brian2 import *
from utils.create_neuron_group import create_neuron_group
from params import cell_params

# Immature granule cell
def create_igc(N=None):
  params = cell_params['igc'].copy()
  params = {**params, "N": N if N is not None else params['N']}
  igc = create_neuron_group(**params)
  return igc

