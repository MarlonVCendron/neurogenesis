import h5py
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.sparse import csr_matrix
from utils.utils import read_connectivity
from os.path import join
from params import results_dir


# old

# filename = join(results_dir, "connectivity_matrices.h5")
# with h5py.File(filename, 'r') as f:
#   group_name = "bc->mgc"
#   row = f[f"{group_name}/row"][:]
#   col = f[f"{group_name}/col"][:]
#   data = f[f"{group_name}/data"][:]

#   shape = (max(row) + 1, max(col) + 1)
#   sparse_matrix = csr_matrix((data, (row, col)), shape=shape)
#   print(np.mean(np.sum(sparse_matrix, axis=1)))
#   print(np.mean(np.sum(sparse_matrix, axis=0)))


conn_i, conn_j = read_connectivity("pca3", "mc")

shape = (max(conn_i) + 1, max(conn_j) + 1)
sparse_matrix = csr_matrix((np.ones(len(conn_i)), (conn_i, conn_j)), shape=shape)

connection_probability_from = np.mean(np.sum(sparse_matrix, axis=1)) / shape[1]
connection_probability_to = np.mean(np.sum(sparse_matrix, axis=0)) / shape[0]
print(connection_probability_from)
print(connection_probability_to)

min_from = np.sum(sparse_matrix, axis=1).min()
max_from = np.sum(sparse_matrix, axis=1).max()
min_to = np.sum(sparse_matrix, axis=0).min()
max_to = np.sum(sparse_matrix, axis=0).max()

print(f"min from: {min_from}, max from: {max_from}")
print(f"min to: {min_to}, max to: {max_to}")

plt.imshow(sparse_matrix.toarray(), aspect="auto", cmap="Greys", interpolation="nearest")
plt.show()
