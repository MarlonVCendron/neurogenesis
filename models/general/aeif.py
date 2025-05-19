from brian2 import *

def aEIF(exponential=True):
  eq_model = Equations(f'''
    dVm/dt = (-I_L  + I_exp - I_syn + I_ext - o) / Cm : volt
    I_syn  = I_ampa + I_nmda + I_gaba                 : amp
    I_L    = g_L * (Vm - E_L)                         : amp
    do/dt  = (a * (Vm - E_L) - o) / tau_o             : amp
  ''')

  if exponential:
    eq_model += 'I_exp  = g_L * DeltaT * exp((Vm-V_th)/DeltaT) : amp'
  else:
    eq_model += 'I_exp  = 0 * amp : amp'

  eq_params = Equations('''
    Cm     : farad    # Membrane capacitance
    g_L    : siemens  # Leak conductance
    E_L    : volt     # Leak reversal potential
    V_th   : volt     # Threshold potential
    V_reset: volt     # Reset potential
    DeltaT : volt     # Slope factor
    a      : siemens  # Subthreshold adaptation
    b      : amp      # Spike-triggered adaptation
    tau_o  : second   # Adaptation time constant
    I_ext  : amp      # External current
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
  reset      = '''
    Vm = V_reset
    o  = o + b
  '''

  refractory = 0 * ms  # A way to have lastspike

  return (eqs, threshold, reset, refractory)
