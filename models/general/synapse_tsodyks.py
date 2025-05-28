from brian2 import *

def synapse_tsodyks(syn_type) : 
  E_val = -86 if syn_type == 'inh' else 0

  eq_reversal = Equations(f'E = {E_val} * mV : volt')

  eq_model = Equations('''
    dx/dt = z / tau_r        : 1 (clock-driven)  # Recovered
    dy/dt = -y / tau_d       : 1 (clock-driven)  # Active
    du/dt = -u / tau_f       : 1 (clock-driven)  # Facilitation
    z     = 1 - x - y        : 1                 # Inactive
    I_syn = g * y * (Vm - E) : amp (summed)
  ''')

  eq_params = Equations('''
    g     : siemens  # Synaptic conductance
    U     : 1        # Portion of available resources utilized on each synaptic event 
    tau_d : second   # Decay time constant
    tau_r : second   # Resource recovery time constant
    tau_f : second   # Resource utilization reduction time constant
  ''')

  on_pre = Equations('''
    u += U * (1 - u)
    y += u * x        # important: update y first
    x += -u * x
  ''')

  eqs = eq_model + eq_params + eq_reversal

  return (eqs, on_pre)