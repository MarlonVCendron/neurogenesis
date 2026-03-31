import os
import h5py
import numpy as np

from params import results_dir

def load_pattern_data(run):
  run_dir = os.path.join(results_dir, run)
  subdirs = [os.path.join(run_dir, d) for d in os.listdir(run_dir) if os.path.isdir(os.path.join(run_dir, d))]

  data = {}

  for subdir in subdirs:
    file_path = os.path.join(subdir, 'patterns.h5')
    run_name = os.path.basename(subdir)

    if not os.path.exists(file_path):
      continue

    with h5py.File(file_path, 'r') as h5file:
      parts = run_name.split('_')
      pattern_idx = int(parts[-1])
      trial = int(parts[-3])
      group = '_'.join(parts[:-4])  # 'control' or 'neurogenesis_0.2'

      has_neurogenesis = 'neurogenesis' in group

      pp_pattern = np.array(h5file['pp_pattern'])
      mgc_pattern = np.array(h5file['mgc_pattern'])
      igc_pattern = np.array(h5file['igc_pattern']) if has_neurogenesis else np.array([])
      pca3_pattern = np.array(h5file['pca3_pattern'])
      in_similarity = np.array(h5file['in_similarity']).item()

      if 'rates' in h5file:
        rates = {ct: np.array(h5file['rates'][ct]) for ct in h5file['rates']}
      else:
        rates = {
          'mgc': np.array(h5file['mgc_rates']),
          'igc': np.array(h5file['igc_rates']) if has_neurogenesis else np.array([]),
          'pca3': np.array(h5file['pca3_rates']),
          'ica3': np.array(h5file['ica3_rates']),
        }

      spike_counts = (
        {ct: np.array(h5file['spike_counts'][ct]) for ct in h5file['spike_counts']}
        if 'spike_counts' in h5file else {}
      )

      if group not in data:
        data[group] = []

      trial_entry = next((t for t in data[group] if t['trial'] == trial), None)
      if not trial_entry:
        trial_entry = {'trial': trial, 'patterns': [], 'original_pattern': None}
        data[group].append(trial_entry)

      pattern = {
        'pp_pattern': pp_pattern,
        'mgc_pattern': mgc_pattern,
        'igc_pattern': igc_pattern,
        'pca3_pattern': pca3_pattern,
        'gc_pattern': np.concatenate((mgc_pattern, igc_pattern)),
        'rates': rates,
        'spike_counts': spike_counts,
        'in_similarity': in_similarity,
      }

      if in_similarity == 1.0:
        trial_entry['original_pattern'] = pattern

      trial_entry['patterns'].append(pattern)

  for key in data:
    data[key].sort(key=lambda x: x['trial'])
    for trial_entry in data[key]:
      trial_entry['patterns'].sort(key=lambda p: p['in_similarity'])

  return data
