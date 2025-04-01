import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

from params import results_dir
from utils.patterns import pattern_separation_degree, activation_degree, correlation_degree

run_02_dir = os.path.join(results_dir, 'run_02')
subdirs = [os.path.join(run_02_dir, d) for d in os.listdir(run_02_dir) if os.path.isdir(os.path.join(run_02_dir, d))]

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

in_sim_dict = {}
# for trial in data['neurogenesis_0.1']:
for trial in data['control']:
  original_inp = trial['original_pattern']['pp_pattern']
  original_out = trial['original_pattern']['gc_pattern']

  for pattern in trial['patterns'][:-1]:
    sim = pattern['in_similarity']
    inp = pattern['pp_pattern']
    out = pattern['gc_pattern']
    s_d = pattern_separation_degree(original_inp, inp, original_out, out)
    # s_d = activation_degree(out)
    # s_d = correlation_degree(original_inp, inp)
    # s_d = correlation_degree(original_out, out)
    
    if sim not in in_sim_dict:
        in_sim_dict[sim] = []
    in_sim_dict[sim].append(s_d)

average_sd = {sim: np.mean(sds) for sim, sds in in_sim_dict.items()}
sorted_in_sim = sorted(average_sd.keys())
sorted_average_sd = [average_sd[sim] for sim in sorted_in_sim]

print(np.std(sorted_average_sd))

plt.figure(figsize=(8, 6))
plt.plot(sorted_in_sim, sorted_average_sd, marker='o')
plt.xlabel('In Similarity')
plt.ylabel('Average Pattern Separation Degree')
plt.title('Average Pattern Separation Degree by In Similarity')
plt.grid(True)
plt.show()


