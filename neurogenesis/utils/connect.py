from brian2 import *
from neurogenesis.models.general import synapse


def Connect(source, target, receptor, condition, delay, K, E, tau_r, tau_d, p=1):
  (eqs, on_pre) = synapse(receptor)

  synapses = Synapses(
      source=source,
      target=target,
      model=eqs,
      on_pre=on_pre,
      delay=delay,
  )

  synapses.connect(condition=condition, p=p)

  synapses.__setattr__(f'K_{receptor}', K)
  synapses.__setattr__(f'E_{receptor}', E)
  synapses.__setattr__(f'tau_{receptor}_r', tau_r)
  synapses.__setattr__(f'tau_{receptor}_d', tau_d) 

  return synapses
