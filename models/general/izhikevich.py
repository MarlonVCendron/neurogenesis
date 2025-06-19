from brian2 import *

def Izhikevich():
  eq_model = Equations('''
    dVm/dt  = (k * (Vm - Vr) * (Vm - Vt) - u + I_total) / Cm : volt
    du/dt   = a * (-u + b * (Vm - Vr))                       : amp
    I_total = - I_syn + I_ext                                : amp
  ''')

  eq_params = Equations('''
    Cm    : farad         # Membrane capacitance
    k     : siemens/volt  # Rate constant of the membrane potential
    a     : hertz         # Rate constant of the recovery variable
    b     : siemens       # Sensitivity of the recovery variable to the subthreshold fluctuations of Vm
    d     : amp           # After-spike reset of u
    Vr    : volt          # Leak reversal potential
    Vt    : volt          # Threshold potential
    Vpeak : volt          # Spike cutoff value
    Vmin  : volt          # Reset potential

    I_ext : amp           # External current
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
