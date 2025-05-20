from brian2 import *
from models.general import AdEx, LIF
from params import cell_params


def create_neuron_group_lif(N, Cm, g_L, E_L, g_ahp_max, tau_ahp, E_ahp, V_th, name):
  lif_eqs, threshold, reset, refractory = LIF()

  neuron = NeuronGroup(
      N          = N,
      model      = lif_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      name       = name,
      method     = 'rk2',
  )

  # Params
  neuron.E_L       = E_L
  neuron.Cm        = Cm
  neuron.g_L       = g_L
  neuron.g_ahp_max = g_ahp_max
  neuron.tau_ahp   = tau_ahp
  neuron.E_ahp     = E_ahp
  neuron.V_th      = V_th

  # Initialize
  neuron.Vm = E_L

  return neuron

def create_neuron_group(N, Cm, g_L, E_L, V_th, DeltaT, a, b, tau_o, V_reset, name):
  exponential = DeltaT != 0
  adex_eqs, threshold, reset, refractory = AdEx(exponential)

  neuron = NeuronGroup(
      N          = N,
      model      = adex_eqs,
      threshold  = threshold,
      reset      = reset,
      refractory = refractory,
      name       = name,
      method     = 'rk2',
  )

  # Params
  neuron.E_L       = E_L
  neuron.Cm        = Cm
  neuron.g_L       = g_L
  neuron.V_th      = V_th
  neuron.V_reset   = V_reset
  neuron.DeltaT    = DeltaT
  neuron.a         = a
  neuron.b         = b
  neuron.tau_o     = tau_o

  # Initialize
  neuron.Vm = E_L

  return neuron
