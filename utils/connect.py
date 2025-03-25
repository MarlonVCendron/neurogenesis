from brian2 import *

from models.general import synapse
from utils.utils import read_connectivity

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

  conn_i, conn_j = read_connectivity(source, target)
  
  if len(conn_i) > 0 and len(conn_j) > 0:
    synapses.connect(i=conn_i, j=conn_j)
  else:
    # This will randomly connect the synapses, even for the same source and target, but different receptors
    synapses.connect(p=p, condition=condition)

  synapses.g_max = g_max
  synapses.E     = E
  synapses.tau_r = tau_r
  synapses.tau_d = tau_d

  return synapses
