import os
import h5py
import numpy as np

from params import results_dir

subdirs = [os.path.join(results_dir, d) for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))]

merged_data = {}

for subdir in subdirs:
  file_path = os.path.join(subdir, 'patterns.h5')

  if os.path.exists(file_path):
    with h5py.File(file_path, 'r') as h5file:
      data = h5file

      pppattern = np.array(data['pppattern'])
      mgc_pattern = np.array(data['mgc_pattern'])
      in_similarity = np.array(data['in_similarity'])
      
      merged_data[subdir] = {
        'pppattern': pppattern,
        'mgc_pattern': mgc_pattern,
        'in_similarity': in_similarity
      }



print(merged_data)
