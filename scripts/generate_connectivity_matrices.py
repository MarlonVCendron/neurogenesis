from brian2 import *
import h5py

from utils.initialize import initialize
from models.general.network import network
from utils.utils import get_synapses, get_connectivity_filepath
from plotting.connectivity_matrices import connectivity_matrices

# NOTE: This script should be run with skip_connectivity_matrices = True
if __name__ == '__main__':
  initialize()
  net = network()
  run(0*ms)
  device.build(run=True)

  synapses = get_synapses(net)

  # connectivity_matrices(net, plot=True)

  for syn in synapses:
    source = syn.source
    target = syn.target
    
    filepath = get_connectivity_filepath(source, target)
    file = h5py.File(filepath, 'w')

    file.create_dataset("i", data=syn.i[:])
    file.create_dataset("j", data=syn.j[:])
    file.close()
    
  
