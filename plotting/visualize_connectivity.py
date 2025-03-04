import h5py
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.sparse import csr_matrix

from os.path import join
from params import results_dir


filename = join(results_dir, "connectivity_matrices.h5")


with h5py.File(filename, 'r') as f:
  group_name = "pp->bc"
  row = f[f"{group_name}/row"][:]
  col = f[f"{group_name}/col"][:]
  data = f[f"{group_name}/data"][:]

  shape = (max(row) + 1, max(col) + 1)
  sparse_matrix = csr_matrix((data, (row, col)), shape=shape)

plt.imshow(sparse_matrix.toarray(), aspect="auto", cmap="Greys", interpolation="nearest")
plt.show()
