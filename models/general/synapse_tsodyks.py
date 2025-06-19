from brian2 import *

def synapse_tsodyks(syn_type, syn_var) : 
  E_val = -86 if syn_type == 'inh' else 0

  eq_reversal = Equations(f'E = {E_val} * mV : volt')

  eq_model = Equations(f'''
    dU/dt = -U / tau_f                   : 1 (clock-driven)  # Resource utilization
    dR/dt = (1 - R - A) / tau_r          : 1 (clock-driven)  # Resource recovery
    dA/dt = -A / tau_d                   : 1 (clock-driven)  # Resource activation
    I     = A * scale * w * g * (Vm - E) : amp

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
    U += U_se * (1 - U)
    A += U * R
    R += -U * R
  '''

  eqs = eq_model + eq_params + eq_reversal

  return (eqs, on_pre)