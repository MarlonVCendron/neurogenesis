from brian2 import *

def get_objects(net, obj_type):
  return sorted(
    [obj for obj in net.objects if isinstance(obj, obj_type)],
    key=lambda obj: obj.name
  )

def get_neurons(net):
  return get_objects(net, NeuronGroup) + get_objects(net, PoissonGroup)

def get_spike_monitors(net):
  return get_objects(net, SpikeMonitor)

def get_rate_monitors(net):
  return get_objects(net, PopulationRateMonitor)

def get_neuron(net, name):
  return next((obj for obj in net.objects if obj.name == name), None)

def get_neuron_monitor(net, name):
  return next((obj for obj in net.objects if isinstance(obj, SpikeMonitor) and obj.source.name == name), None)