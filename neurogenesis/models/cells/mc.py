from brian2 import *
from neurogenesis.models.general.lif import LIF

params = {
    "Cm"        : 206.0 * pF,
    "g_L"       : 5.0 * nS,
    "E_L"       : -62.0 * mV,
    "g_ahp_max" : 78.0 * nS,
    "tau_ahp"   : 10.0 * ms,
    "E_ahp"     : -80.0 * mV,
    "V_th"      : -32.0 * mV,
    "I_ampa"    : -250 * pA,
    "I_nmda"    : 0 * pA,
    "I_gaba"    : 0 * pA,
}

lif_eqs = LIF()

mc = NeuronGroup(
    10,
    model      = lif_eqs,
    threshold  = 'Vm > V_th',
    reset      = 'Vm = E_L',
    method     = 'rk2',
    refractory = 0*ms          # A way to have lastspike
)
for param, value in params.items():
  setattr(mc, param, value)

mc.Vm = mc.E_L
