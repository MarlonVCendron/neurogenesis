from brian2 import *
from neurogenesis.models.general import LIF
from neurogenesis.params import cell_params

# Basket cell
def create_bc(N):
  lif_eqs, threshold, reset, refractory = LIF()
  
  bc = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in cell_params['bc'].items():
    setattr(bc, param, value)
  
  bc.Vm = bc.E_L

  return bc
  