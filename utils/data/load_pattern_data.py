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

    if os.path.exists(file_path):
      with h5py.File(file_path, 'r') as h5file:
        parts = run_name.split('_')
        pattern = int(parts[-1])
        trial = int(parts[-3])
        group = '_'.join(parts[:-4]) # 'control' or 'neurogenesis_0.2'

        has_neurogenesis = 'neurogenesis' in group

        pp_pattern = np.array(h5file['pp_pattern'])
        mgc_pattern = np.array(h5file['mgc_pattern'])
        igc_pattern = np.array(h5file['igc_pattern']) if has_neurogenesis else np.array([])
        in_similarity = np.array(h5file['in_similarity']).item()

        if group not in data:
          data[group] = []

        trial_entry = next((t for t in data[group] if t['trial'] == trial), None)
        if not trial_entry:
          trial_entry = {'trial': trial, 'patterns': [], 'original_pattern': None}

        pattern = {
            'pp_pattern': pp_pattern,
            'mgc_pattern': mgc_pattern,
            'igc_pattern': igc_pattern,
            'in_similarity': in_similarity,
            'gc_pattern': np.concatenate((mgc_pattern, igc_pattern)) 
        }

        if (in_similarity == 1.0):
          trial_entry['original_pattern'] = pattern

        trial_entry['patterns'].append(pattern)

        data[group].append(trial_entry)

  for key in data:
    data[key].sort(key=lambda x: x['trial'])
    for trial_entry in data[key]:
      trial_entry['patterns'].sort(key=lambda p: p['in_similarity'])
  
  return data