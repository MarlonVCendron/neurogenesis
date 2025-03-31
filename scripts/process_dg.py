import os
import h5py
import numpy as np

from params import results_dir
from utils.patterns import pattern_separation_degree

subdirs = [os.path.join(results_dir, d) for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))]

data = {}

for subdir in subdirs:
  file_path = os.path.join(subdir, 'patterns.h5')
  run_name = os.path.basename(subdir)

  if os.path.exists(file_path):
    with h5py.File(file_path, 'r') as h5file:
      pp_pattern = np.array(h5file['pp_pattern'])
      mgc_pattern = np.array(h5file['mgc_pattern'])
      in_similarity = np.array(h5file['in_similarity']).item()

      parts = run_name.split('_')
      group = parts[0]  # 'control' or 'neurogenesis'
      trial = int(parts[2])
      pattern = int(parts[-1])

      if group not in data:
        data[group] = []

      trial_entry = next((t for t in data[group] if t['trial'] == trial), None)
      if not trial_entry:
        trial_entry = {'trial': trial, 'patterns': [], 'original_pattern': None}
        data[group].append(trial_entry)

      pattern = {
          'pp_pattern': pp_pattern,
          'mgc_pattern': mgc_pattern,
          'in_similarity': in_similarity
      }

      if (in_similarity == 1.0):
        trial_entry['original_pattern'] = pattern

      trial_entry['patterns'].append(pattern)

# for key in merged_data:
#   merged_data[key].sort(key=lambda x: x['trial'])
for key in data:
  data[key].sort(key=lambda x: x['trial'])
  # Sort patterns within each trial by in_similarity
  for trial_entry in data[key]:
    trial_entry['patterns'].sort(key=lambda p: np.mean(p['in_similarity']), reverse=True)


print(data['control'][0]['original_pattern'])
