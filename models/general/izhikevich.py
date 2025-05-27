from brian2 import *

def Izhikevich():
  eq_model = Equations('''
    dVm/dt = (K * (Vm - Vr) * (Vm - V_th) - U + I) / Cm : volt
    du/dt  = A * (-u + B * (Vm - Vr))                   : 1
    I      = I_syn + I_ext                              : amp
    
    # Matching units
    A      = a / ms                                     : hertz
    B      = b / mV                                     : volt**-1
    K      = k * nS / mV                                : siemens / volt
    U      = u * pA                                     : amp
  ''')

  eq_params = Equations('''
    Cm      : farad       # Membrane capacitance
    k       : 1           # Rate constant of the membrane potential
    a       : 1           # Rate constant of the recovery variable
    b       : 1           # Sensitivity of the recovery variable to the subthreshold fluctuations of Vm
    d       : 1           # After-spike reset of u
    Vr      : volt        # Leak reversal potential
    V_th    : volt        # Threshold potential
    Vpeak   : volt        # Spike cutoff value
    Vmin    : volt        # Reset potential

    I_ext   : amp         # External current
    eta     : mmolar**-1  # Mg concentration sensitivity
    gamma   : volt**-1    # Mg concentration steepness
    Mg_conc : mmolar      # Mg concentration
  ''')

  # Multiple synapses can't be summed over the same neuron variable, so we need to
  # create a new variable for each synapse
  eq_syn = Equations('''
    I_syn      = I_ampa + I_nmda + I_gaba                  : amp
    I_ampa     = I_ampa_1 + I_ampa_2 + I_ampa_3 + I_ampa_4 : amp
    I_nmda     = I_nmda_1 + I_nmda_2 + I_nmda_3 + I_nmda_4 : amp
    I_gaba     = I_gaba_1 + I_gaba_2                       : amp
    I_ampa_1   : amp
    I_ampa_2   : amp
    I_ampa_3   : amp
    I_ampa_4   : amp
    I_nmda_1   : amp
    I_nmda_2   : amp
    I_nmda_3   : amp
    I_nmda_4   : amp
    I_gaba_1   : amp
    I_gaba_2   : amp
    alpha_ampa : second**-1
    alpha_nmda : second**-1
    alpha_gaba : second**-1
  ''')

  eqs = eq_model + eq_params + eq_syn

  threshold = 'Vm >= Vpeak'
  reset = '''
    Vm = Vmin
    u += d
  '''

  refractory = 0 * ms

  return (eqs, threshold, reset, refractory)
