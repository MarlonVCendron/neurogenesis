from brian2 import *
from neurogenesis.models.general import LIF
from neurogenesis.params import cell_params

# Mature granule cell
def create_mgc(N):
  lif_eqs, threshold, reset, refractory = LIF()
  
  mgc = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in cell_params['mgc'].items():
    setattr(mgc, param, value)
  
  mgc.Vm = mgc.E_L
  
  return mgc
