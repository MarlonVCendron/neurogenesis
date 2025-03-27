from brian2 import *
from os.path import join

from utils.args_config import args

# Number of trials
trials = 1 # 30

# Whether the network has immature GCs
has_igc = args.neurogenesis

# Number of lamellae
N_lamellae = 20

# IGC connection probability
igc_conn = 1.0 if has_igc else 0.0

# Rate of EC neurons
pp_rate = 40 * Hz

# Simulation time for the network to settle
break_time = 300 * ms
# Simulation time when activity is recorded
stim_time = 1000 * ms

# Whether to skip the loading of connectivity matrices
skip_connectivity_matrices = False

base_dir = './'
results_dir = join(base_dir, 'res')
connectivity_dir = join(base_dir, 'connectivity')