from brian2 import *
from utils.args_config import args

REVERSAL_POTENTIAL = { 'nmda':  0 * mV, 'ampa': 0 * mV, 'gaba': -86 * mV }

def synapse(receptor) : 
  R        = receptor         # e.g. 'ampa_1'
  receptor = R.split('_')[0]  # e.g. 'ampa'

  E_val = REVERSAL_POTENTIAL[receptor] / mV

  if receptor == 'nmda':
    eq_I_synapse = Equations('I_synapse = I_pre_sat / (1 + Mg_conc*eta*exp(-gamma*Vm)) : amp')
  else:
    eq_I_synapse = Equations('I_synapse = I_pre_sat : amp')
  
  eq_model = Equations(f'''
    I_pre_sat  = g_syn * (Vm - E)                 : amp
    g_syn      = g_max * s                        : siemens
    ds/dt      = -s / tau_d + h * alpha * (1 - s) : 1 (clock-driven)
    dh/dt      = -h / tau_r                       : 1 (clock-driven)

    I_{R}_post = I_synapse                        : amp (summed)
  ''')

  eq_params = Equations(f'''
    g_max : siemens                        # Synaptic strength
    tau_r : second                         # Rise time
    tau_d : second                         # Decay time
    w     = 1                : 1           # Synaptic weight
    E     = {E_val} * mV     : volt        # Reversal potential
    alpha = alpha_{receptor} : second**-1  # Scaling factor
  ''')

  on_pre = 'h += w'

  eqs = eq_model + eq_params + eq_I_synapse

  return (eqs, on_pre)