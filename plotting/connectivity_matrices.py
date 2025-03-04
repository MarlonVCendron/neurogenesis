from brian2 import *
import scipy.sparse as sp
import h5py
from os.path import join

from utils.utils import get_synapses
from params import results_dir

def connectivity_matrices(net, plot=False, filename="connectivity_matrices.h5"):
  synapses = get_synapses(net)
  file = h5py.File(join(results_dir,filename), 'w')

  for syn in synapses:
    source_name = syn.source.name
    target_name = syn.target.name
    pre = syn.i
    post = syn.j

    connectivity_matrix = sp.coo_matrix((np.ones(len(pre)), (pre, post)), shape=(len(syn.source), len(syn.target)))
    dense_matrix = connectivity_matrix.toarray()

    group_name = f"{source_name}->{target_name}"
    if(group_name in file):
      continue
    group = file.create_group(group_name)
    group.create_dataset("row", data=connectivity_matrix.row)
    group.create_dataset("col", data=connectivity_matrix.col)
    group.create_dataset("data", data=connectivity_matrix.data)
    group.attrs["shape"] = connectivity_matrix.shape

    # Plot connection matrix
    if plot:
      plt.figure()
      plt.matshow(dense_matrix, cmap='Greys', fignum=False)
      plt.title(f'{source_name} → {target_name}')
      plt.grid(True, which="both", color="gray", linestyle=":", linewidth=0.5)
      plt.xlabel(target_name)
      plt.ylabel(source_name)
      plt.show()
