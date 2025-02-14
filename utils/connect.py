from brian2 import *
from models.general import synapse


def Connect(source, target, receptor, delay, g_max, E, tau_r, tau_d, condition=None, p=1):
  (eqs, on_pre) = synapse(receptor)

  synapses = Synapses(
      source=source,
      target=target,
      model=eqs,
      on_pre=on_pre,
      delay=delay,
      method='rk2',
  )

  synapses.connect(condition=condition, p=p)

  synapses.g_max = g_max
  synapses.E     = E
  synapses.tau_r = tau_r
  synapses.tau_d = tau_d

  return synapses
