from brian2 import *
import scipy.sparse as sp


def connectivity_matrices(net):
  synapses = [obj for obj in net.objects if isinstance(obj, Synapses)]
  for syn in synapses:
    source_name = syn.source.name
    target_name = syn.target.name
    pre = syn.i
    post = syn.j

    connectivity_matrix = sp.coo_matrix((np.ones(len(pre)), (pre, post)), shape=(len(syn.source), len(syn.target)))
    dense_matrix = connectivity_matrix.toarray()

    # Plot connection matrix
    plt.figure()
    plt.matshow(dense_matrix, cmap='Greys', fignum=False)
    plt.title(f'{source_name} → {target_name}')
    plt.grid(True, which="both", color="gray", linestyle=":", linewidth=0.5)
    plt.xlabel(target_name)
    plt.ylabel(source_name)
    plt.show()
