from brian2 import *
from models.general import AdEx, LIF, expIF
from utils.args_config import args

alpha_ampa = args.ampa * ms**-1
alpha_nmda = args.nmda * ms**-1
alpha_gaba = args.gaba * ms**-1

eta     = 0.28 * mM**-1
gamma   = 0.072 * mV**-1
Mg_conc = 1 * mM

def create_neuron_group_lif(
  N,
  Cm,
  g_L,
  E_L,
  g_ahp_max,
  tau_ahp,
  E_ahp,
  V_th,
  name,
  alpha_ampa=alpha_ampa,
  alpha_nmda=alpha_nmda,
  alpha_gaba=alpha_gaba,
  eta=eta,
  gamma=gamma,
  Mg_conc=Mg_conc
):
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
  neuron.alpha_ampa = alpha_ampa
  neuron.alpha_nmda = alpha_nmda
  neuron.alpha_gaba = alpha_gaba
  neuron.eta        = eta
  neuron.gamma      = gamma
  neuron.Mg_conc    = Mg_conc

  # Initialize
  neuron.Vm = E_L

  return neuron

def create_neuron_group_adex(
  N,
  Cm,
  g_L,
  E_L,
  V_th,
  DeltaT,
  a,
  b,
  tau_o,
  V_reset,
  name,
  alpha_ampa=alpha_ampa,
  alpha_nmda=alpha_nmda,
  alpha_gaba=alpha_gaba,
  eta=eta,
  gamma=gamma,
  Mg_conc=Mg_conc
):
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
  neuron.alpha_ampa = alpha_ampa
  neuron.alpha_nmda = alpha_nmda
  neuron.alpha_gaba = alpha_gaba
  neuron.eta        = eta
  neuron.gamma      = gamma
  neuron.Mg_conc    = Mg_conc

  # Initialize
  neuron.Vm = E_L

  return neuron

def create_neuron_group_expif(
  N,
  Cm,
  g_L,
  E_L,
  V_th,
  V_reset,
  DeltaT,
  name,
  alpha_ampa=alpha_ampa,
  alpha_nmda=alpha_nmda,
  alpha_gaba=alpha_gaba,
  eta=eta,
  gamma=gamma,
  Mg_conc=Mg_conc
):
  expif_eqs, threshold, reset, refractory = expIF()

  neuron = NeuronGroup(
      N          = N,
      model      = expif_eqs,
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
  neuron.alpha_ampa = alpha_ampa
  neuron.alpha_nmda = alpha_nmda
  neuron.alpha_gaba = alpha_gaba
  neuron.eta        = eta
  neuron.gamma      = gamma
  neuron.Mg_conc    = Mg_conc

  # Initialize
  neuron.Vm = E_L

  return neuron

def create_neuron_group(*args, **kwargs):
  model = kwargs.pop('model')
  if model == 'lif':
    return create_neuron_group_lif(**kwargs)
  elif model == 'adex':
    return create_neuron_group_adex(**kwargs)
  elif model == 'expif':
    return create_neuron_group_expif(**kwargs)