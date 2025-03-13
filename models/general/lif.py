from brian2 import *

def LIF():
  id = randint(0, 1000000)

  eq_model = Equations(f'''
    dVm/dt = (-I_L -I_ahp -I_syn + I_ext + I_noise) / Cm  : volt
    I_L    = g_L * (Vm - E_L)                             : amp
    I_ahp  = g_ahp * (Vm - E_ahp)                         : amp
    g_ahp  = g_ahp_max * exp(- (t - lastspike) / tau_ahp) : siemens
    I_syn  = I_ampa + I_nmda + I_gaba                     : amp

    dI_noise/dt = (mu_noise - I_noise) / tau_noise + sigma_noise * (sqrt(2/tau_noise) * xi_{id}) : amp
  ''')

  eq_params = Equations('''
    Cm        : farad    # Membrane capacitance
    g_L       : siemens  # Leak conductance
    E_L       : volt     # Leak reversal potential
    g_ahp_max : siemens  # Maximum AHP conductance
    tau_ahp   : second   # AHP time constant
    E_ahp     : volt     # AHP reversal potential
    V_th      : volt     # Threshold potential
    I_ext     : amp      # External current

    tau_noise   = 15 * ms : second  # Noise time constant 
    sigma_noise = 5 * pA  : amp     # Noise standard deviation
    mu_noise    = 0 * pA  : amp     # Noise mean
  ''')

  # Multiple synapses can't be summed over the same neuron variable, so we need to
  # create a new variable for each synapse
  eq_syn = Equations('''
    I_ampa   = I_ampa_1 + I_ampa_2 + I_ampa_3 + I_ampa_4 : amp
    I_nmda   = I_nmda_1 + I_nmda_2 + I_nmda_3 + I_nmda_4 : amp
    I_gaba   = I_gaba_1 + I_gaba_2                       : amp
    I_ampa_1 : amp
    I_ampa_2 : amp
    I_ampa_3 : amp
    I_ampa_4 : amp
    I_nmda_1 : amp
    I_nmda_2 : amp
    I_nmda_3 : amp
    I_nmda_4 : amp
    I_gaba_1 : amp
    I_gaba_2 : amp
  ''')

  eqs        = eq_model + eq_params + eq_syn
  threshold  = 'Vm > V_th'
  reset      = 'Vm = E_L'
  refractory = 0 * ms                # A way to have lastspike

  return (eqs, threshold, reset, refractory)
