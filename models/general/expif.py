from brian2 import *

def expIF():
  eq_model = Equations(f'''
    dVm/dt = (-I_L  + I_exp - I_syn + I_ext) / Cm : volt (unless refractory)
    I_syn  = I_ampa + I_nmda + I_gaba             : amp
    I_exp  = g_L * DeltaT * exp((Vm-V_th)/DeltaT) : amp
    I_L    = g_L * (Vm - E_L)                     : amp
  ''')

  eq_params = Equations('''
    Cm      : farad       # Membrane capacitance
    g_L     : siemens     # Leak conductance
    E_L     : volt        # Leak reversal potential
    V_th    : volt        # Threshold potential
    V_reset : volt        # Reset potential
    DeltaT  : volt        # Slope factor
    I_ext   : amp         # External current
    eta     : mmolar**-1  # Mg concentration sensitivity
    gamma   : volt**-1    # Mg concentration steepness
    Mg_conc : mmolar      # Mg concentration
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
    alpha_ampa : second**-1
    alpha_nmda : second**-1
    alpha_gaba : second**-1
  ''')

  eqs        = eq_model + eq_params + eq_syn

  threshold  = 'Vm > V_th'
  reset      = 'Vm = V_reset'

  return (eqs, threshold, reset)
