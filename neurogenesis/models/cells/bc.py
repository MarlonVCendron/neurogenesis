from brian2 import *
from neurogenesis.models.general.lif import LIF

params = {
    "Cm"        : 232.6 * pF,
    "g_L"       : 23.2 * nS,
    "E_L"       : -62.0 * mV,
    "g_ahp_max" : 76.9 * nS,
    "tau_ahp"   : 2.0 * ms,
    "E_ahp"     : -75.0 * mV,
    "V_th"      : -52.5 * mV,
    "I_ampa"    : -250 * pA,
    "I_nmda"    : 0 * pA,
    "I_gaba"    : 0 * pA,
}

def create_bc(N=1):
  lif_eqs, threshold, reset, refractory = LIF()
  
  bc = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      method     = 'rk2',
  )
  for param, value in params.items():
    setattr(bc, param, value)
  
  bc.Vm = bc.E_L

  return bc
  