import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

from params import results_dir
from utils.patterns import pattern_separation_degree, activation_degree, correlation_degree

run_01_dir = os.path.join(results_dir, 'run_01')
subdirs = [os.path.join(run_01_dir, d) for d in os.listdir(run_01_dir) if os.path.isdir(os.path.join(run_01_dir, d))]

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

      pattern = {
          'pp_pattern': pp_pattern,
          'mgc_pattern': mgc_pattern,
          'in_similarity': in_similarity
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
for trial in data['control']:
  original_inp = trial['original_pattern']['pp_pattern']
  original_out = trial['original_pattern']['mgc_pattern']

  for pattern in trial['patterns'][:-1]:
    sim = pattern['in_similarity']
    inp = pattern['pp_pattern']
    out = pattern['mgc_pattern'] 
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


