from brian2 import *
from neurogenesis.models.general import LIF
from neurogenesis.params import cell_params

# Mossy cell
def create_mc(N):
  lif_eqs, threshold, reset, refractory = LIF()

  mc = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in cell_params['mc'].items():
    setattr(mc, param, value)

  mc.Vm = mc.E_L

  return mc
