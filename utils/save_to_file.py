from os import makedirs
from os.path import join
import h5py

from utils.patterns import get_pp_pattern

def save_to_file(results_directory, pattern, mgc_pattern, igc_pattern):
  in_similarity = pattern['similarity']
  pp_pattern = get_pp_pattern(pattern) 
  
  makedirs(results_directory, exist_ok=True)

  with h5py.File(join(results_directory, 'patterns.h5'), 'w') as f:
    f.create_dataset('pp_pattern', data=pp_pattern)
    f.create_dataset('mgc_pattern', data=mgc_pattern)
    f.create_dataset('igc_pattern', data=igc_pattern)
    f.create_dataset('in_similarity', data=in_similarity)
  