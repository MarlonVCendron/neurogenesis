from brian2 import *

# These equations are all wrong
def synapse(receptor):
  R = receptor

  eq_model = Equations(f'''
    I_{R}_syn   = g_{R} * (Vm - E_{R})                          : amp
    g_{R}       = K_{R} * s_{R}                                 : siemens
    s_{R}       = (y_{R}_d - y_{R}_r) / (tau_{R}_d - tau_{R}_r) : Hz
    dy_{R}_r/dt = -y_{R}_r / tau_{R}_r                          : 1 (clock-driven)
    dy_{R}_d/dt = -y_{R}_d / tau_{R}_d                          : 1 (clock-driven)
    w_{R}       = 1                                             : 1                 # Synaptic weight
  ''')

  eq_params = Equations(f'''
    K_{R}     : siemens/hertz  # Synaptic strength
    E_{R}     : volt           # Reversal potential
    tau_{R}_r : second         # Rise time
    tau_{R}_d : second         # Decay time
  ''')

  on_pre = f'''
    y_{R}_r += w_{R}
    y_{R}_d += w_{R}
    I_{R}   += I_{R}_syn # wrong
  '''

  eqs = eq_model + eq_params

  return (eqs, on_pre)
