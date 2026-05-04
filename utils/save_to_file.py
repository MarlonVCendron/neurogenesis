from os import makedirs
from os.path import join
import h5py

from utils.patterns import get_pp_pattern

def save_to_file(results_directory, pattern, mgc_pattern, igc_pattern, pca3_pattern, rates, spike_counts, spike_times):
  in_similarity = pattern['similarity']
  pp_pattern = get_pp_pattern(pattern)

  makedirs(results_directory, exist_ok=True)

  with h5py.File(join(results_directory, 'patterns.h5'), 'w') as f:
    f.create_dataset('pp_pattern', data=pp_pattern)
    f.create_dataset('mgc_pattern', data=mgc_pattern)
    f.create_dataset('igc_pattern', data=igc_pattern)
    f.create_dataset('pca3_pattern', data=pca3_pattern)
    f.create_dataset('in_similarity', data=in_similarity)

    rates_grp = f.create_group('rates')
    for cell_type, data in rates.items():
      rates_grp.create_dataset(cell_type, data=data)

    counts_grp = f.create_group('spike_counts')
    for cell_type, data in spike_counts.items():
      counts_grp.create_dataset(cell_type, data=data)

    st_grp = f.create_group('spike_times')
    for cell_type, data in spike_times.items():
      ct_grp = st_grp.create_group(cell_type)
      ct_grp.create_dataset('times_ms', data=data['times_ms'])
      ct_grp.create_dataset('indices', data=data['indices'])
