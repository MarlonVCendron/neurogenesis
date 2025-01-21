from brian2 import *
from neurogenesis.models.general import LIF
from neurogenesis.params import cell_params

# Immature granule cell
def create_igc(N):
  lif_eqs, threshold, reset, refractory = LIF()
  
  igc = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in cell_params['igc'].items():
    if param == 'N':
      continue
    setattr(igc, param, value)
  
  igc.Vm = igc.E_L
  
  return igc
