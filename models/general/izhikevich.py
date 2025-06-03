from brian2 import *

def Izhikevich():
  eq_model = Equations('''
    dVm/dt = (K * (Vm - Vr) * (Vm - Vt) - U + I) / Cm : volt
    du/dt  = A * (-u + B * (Vm - Vr))                 : 1
    I      = - I_syn + I_ext                            : amp
    
    # Matching units
    A      = a / ms                                   : hertz
    B      = b / mV                                   : volt**-1
    K      = k * nS / mV                              : siemens / volt
    U      = u * pA                                   : amp
  ''')

  eq_params = Equations('''
    Cm      : farad       # Membrane capacitance
    k       : 1           # Rate constant of the membrane potential
    a       : 1           # Rate constant of the recovery variable
    b       : 1           # Sensitivity of the recovery variable to the subthreshold fluctuations of Vm
    d       : 1           # After-spike reset of u
    Vr      : volt        # Leak reversal potential
    Vt      : volt        # Threshold potential
    Vpeak   : volt        # Spike cutoff value
    Vmin    : volt        # Reset potential

    I_ext   : amp         # External current
  ''')

  # Multiple synapses can't be summed over the same neuron variable, so we need to
  # create a new variable for each synapse
  eq_syn = Equations('''
    I_syn   = I_syn_1 + I_syn_2 + I_syn_3 + I_syn_4 + I_syn_5 + I_syn_6 : amp
    I_syn_1 : amp
    I_syn_2 : amp
    I_syn_3 : amp
    I_syn_4 : amp
    I_syn_5 : amp
    I_syn_6 : amp
  ''')

  eqs = eq_model + eq_params + eq_syn

  threshold = 'Vm >= Vpeak'
  reset = '''
    Vm = Vmin
    u += d
  '''

  refractory = 0 * ms

  return (eqs, threshold, reset, refractory)
