from brian2 import *
from os.path import join
import h5py

from params import connectivity_dir, skip_connectivity_matrices, has_igc, igc_conn

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

def get_synapses(net):
  return get_objects(net, Synapses)

def get_connectivity_filepath(source, target):
  filename = f"{source.name}_{target.name}.h5"
  directory = f'neurogenesis_{igc_conn}' if has_igc else 'control'
  return join(connectivity_dir, directory, filename)

def read_connectivity(source, target):
  conn_i = []
  conn_j = []

  try:
    if skip_connectivity_matrices:
      raise Exception('Skipping connectivity matrices')

    filepath = get_connectivity_filepath(source, target)
    file = h5py.File(filepath, 'r')
    conn_i = file['i'][:]
    conn_j = file['j'][:]
    file.close()
  except:
    print(f'Skipping connectivity matrix for : {source.name} -> {target.name}')

  return conn_i, conn_j

neuron_ordering = ['pp', 'mgc', 'igc', 'mc', 'bc', 'hipp', 'pca3', 'ica3']