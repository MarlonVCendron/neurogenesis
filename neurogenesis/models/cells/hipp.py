from brian2 import *
from neurogenesis.models.general.lif import LIF

params = {
    "Cm"        : 94.3 * pF,
    "g_L"       : 2.7 * nS,
    "E_L"       : -65.0 * mV,
    "g_ahp_max" : 52.0 * nS,
    "tau_ahp"   : 5.0 * ms,
    "E_ahp"     : -75.0 * mV,
    "V_th"      : -9.4 * mV,
    "I_ampa"    : 0 * pA,
    "I_nmda"    : 0 * pA,
    "I_gaba"    : 0 * pA,
}

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
  for param, value in params.items():
    setattr(hipp, param, value)

  hipp.Vm = hipp.E_L

  return hipp
