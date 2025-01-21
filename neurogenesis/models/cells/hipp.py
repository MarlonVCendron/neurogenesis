from brian2 import *
from neurogenesis.models.general import LIF
from neurogenesis.params import cell_params

# Hilar perforant path-associated cell
def create_hipp(N):
  lif_eqs, threshold, reset, refractory = LIF()

  hipp = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in cell_params['hipp'].items():
    setattr(hipp, param, value)

  hipp.Vm = hipp.E_L

  return hipp
