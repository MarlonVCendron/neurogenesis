from brian2 import *


def get_neurons(net):
  return sorted(
    [obj for obj in net.objects if (isinstance(obj, PoissonGroup) or isinstance(obj, NeuronGroup))],
    key=lambda ng: ng.name
  )

def get_spike_monitors(net):
  return sorted(
    [obj for obj in net.objects if isinstance(obj, SpikeMonitor)],
    key=lambda sm: sm.source.name
  )

def get_neuron(net, name):
  return next((obj for obj in net.objects if obj.name == name), None)

def get_neuron_monitor(net, name):
  return next((obj for obj in net.objects if isinstance(obj, SpikeMonitor) and obj.source.name == name), None)