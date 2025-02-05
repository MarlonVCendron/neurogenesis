from brian2 import *


def get_neurons(net):
  return sorted(
    [obj for obj in net.objects if (isinstance(obj, PoissonGroup) or isinstance(obj, NeuronGroup))],
    key=lambda ng: ng.name
  )
