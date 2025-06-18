from brian2 import *

def synapse_tsodyks(syn_type, syn_var) : 
  E_val = -86 if syn_type == 'inh' else 0

  eq_reversal = Equations(f'E = {E_val} * mV : volt')

  eq_model = Equations(f'''
    dv/dt = -v / tau_f               : 1 (clock-driven)    # Resource utilization
    dx/dt = (1 - x) / tau_r          : 1 (clock-driven)    # Resource recovery
    dI/dt = -I / tau_d               : amp (clock-driven)  # Synaptic current
    A     = scale * w * g * (Vm - E) : amp

    I_syn_{syn_var}_post = I : amp (summed)
  ''')

  eq_params = Equations('''
    g     : siemens  # Synaptic conductance
    U_se  : 1        # Portion of available resources utilized on each synaptic event 
    tau_d : second   # Decay time constant (synaptic current)
    tau_r : second   # Resource recovery time constant
    tau_f : second   # Resource utilization reduction time constant
    scale : 1        # Scale factor
    w     : 1        # Weight
  ''')

  # Order is important here
  on_pre = '''
    v += U_se * (1 - v)
    x += -v * x
    I += v * x * A
  '''

  eqs = eq_model + eq_params + eq_reversal

  return (eqs, on_pre)