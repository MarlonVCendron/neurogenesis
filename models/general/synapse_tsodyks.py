from brian2 import *

def synapse_tsodyks(syn_type, syn_var) : 
  E_val = -86 if syn_type == 'inh' else 0

  eq_reversal = Equations(f'E = {E_val} * mV : volt')

  eq_model = Equations(f'''
    dx/dt     = z / tau_r        : 1 (clock-driven)  # Recovered
    dy/dt     = -y / tau_d       : 1 (clock-driven)  # Active
    dv/dt     = -v / tau_f       : 1 (clock-driven)  # Facilitation
    z         = 1 - x - y        : 1                 # Inactive
    I_synapse = g * y * (Vm - E) : amp

    I_syn_{syn_var}_post = I_synapse : amp (summed)
  ''')

  eq_params = Equations('''
    g     : siemens  # Synaptic conductance
    U_se  : 1        # Portion of available resources utilized on each synaptic event 
    tau_d : second   # Decay time constant
    tau_r : second   # Resource recovery time constant
    tau_f : second   # Resource utilization reduction time constant
  ''')

  # Order is important here
  on_pre = '''
    v += U_se * (1 - v)
    y += v * x
    x += -v * x
  '''

  eqs = eq_model + eq_params + eq_reversal

  return (eqs, on_pre)