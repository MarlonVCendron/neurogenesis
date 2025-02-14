from os import makedirs
from os.path import join
import numpy as np
import h5py

def save_to_file(results_directory, pattern, mgc_pattern):
  in_similarity = pattern['similarity']
  ec_pattern = pattern['rates'] 
  
  makedirs(results_directory, exist_ok=True)

  with h5py.File(join(results_directory, 'patterns.h5'), 'w') as f:
    f.create_dataset('ec_pattern', data=ec_pattern)
    f.create_dataset('mgc_pattern', data=mgc_pattern)
    f.create_dataset('in_similarity', data=in_similarity)
  