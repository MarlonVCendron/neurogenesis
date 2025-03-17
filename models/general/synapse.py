from brian2 import *

def synapse(receptor):
  R = receptor
  is_nmda = R.startswith('nmda')
  is_ampa = R.startswith('ampa')


  if is_nmda:
    eq_current = Equations('''
      I_synapse = I_s / (1 + exp(-gamma * Vm) * (1.0/3.57)) : amp
      gamma     = 0.072 * mV**-1                            : volt**-1
    ''')
  else:
    eq_current = Equations('''
      I_synapse = I_s : amp
    ''')


  eq_model = Equations(f'''
    I_s        = g_syn * (Vm - E)                          : amp
    g_syn      = g_max * g                                 : siemens
    dg/dt      = (h * alpha) / (tau_r * tau_d) - g / tau_r : 1 (clock-driven)
    dh/dt      = -h / tau_d                                : 1 (clock-driven)
    I_{R}_post = I_synapse                                 : amp (summed)

    # dg/dt     = (h *f* (tau_d-tau_r))/((tau_r*tau_d)) - g/tau_r : 1 (clock-driven)
    # t_peak    = log(tau_d/tau_r) / ((1/tau_r) - (1/tau_d))      : second
    # f         = 1/ (exp(-t_peak/tau_d) - exp(-t_peak/tau_r))    : 1
  ''')

  eq_params = Equations('''
    g_max : siemens           # Synaptic strength
    E     : volt              # Reversal potential
    tau_r : second            # Rise time
    tau_d : second            # Decay time
    w     = 1       : 1       # Synaptic weight
    alpha = 10 * ms : second
  ''')

  on_pre = 'h += w'

  eqs = eq_model + eq_params + eq_current

  return (eqs, on_pre)