import numpy as np
import matplotlib.pyplot as plt

from utils.patterns import pattern_separation_degree, activation_degree, correlation_degree
from utils.data import load_pattern_data

data = load_pattern_data('run_03')

in_sim_dict = {}
for trial in data['neurogenesis_1.0']:
# for trial in data['control']:
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


