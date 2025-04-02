from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from utils.utils import read_connectivity
from utils.patterns import generate_pattern

np.random.seed(1)

pp, igc = read_connectivity('pp', 'igc')

pattern = generate_pattern(p=0.1, N=400)

pp_pattern = pattern

pattern_indices = np.where(pp_pattern == 1)[0]

# active_con_indices = np.where(np.isin(pp, pattern_indices))
active_con_indices = np.where(np.isin(pp, pattern_indices))

active_igc_con = igc[active_con_indices]

igc_indices, igc_counts = np.unique(active_igc_con, return_counts=True)
unique_counts, counts = np.unique(igc_counts, return_counts=True)

total = np.sum(counts)
print(f'Total: {total}')

plt.bar(unique_counts, counts/np.sum(counts), color='blue', alpha=0.7)

plt.xlabel('Value')
plt.ylabel('Count')
plt.title('Histogram of Value Counts')
plt.show()