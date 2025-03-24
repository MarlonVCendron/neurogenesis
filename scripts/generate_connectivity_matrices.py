from brian2 import *
from os.path import join
import h5py

from utils.initialize import initialize
from params import connectivity_dir
from models.general.network import network
from utils.utils import get_synapses
from plotting.connectivity_matrices import connectivity_matrices

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
    
    W = np.full((len(source), len(target)), np.nan)
    W[syn.i[:], syn.j[:]] = syn.w[:]

    filename = f"{source.name}_{target.name}.h5"
    file = h5py.File(join(connectivity_dir,filename), 'w')

    file.create_dataset("W", data=W)
    file.close()
    
  
