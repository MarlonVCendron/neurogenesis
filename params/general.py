from brian2 import *
from os.path import join

from utils.args_config import args

# Number of trials
trials = 1 if args.single_run else args.trials

# Percentage of active neurons in a pattern
active_p = args.active_p

# Whether the network has immature GCs
has_igc = args.neurogenesis

# Number of lamellae
N_lamellae = 20

# IGC connectivity fraction
igc_conn = args.igc_conn if has_igc else 0.0

# Rate of EC neurons
pp_rate = 40 * Hz

# Simulation time for the network to settle
break_time = 300 * ms
# Simulation time when activity is recorded
stim_time = 1000 * ms

# Whether to skip the loading of connectivity matrices
skip_connectivity_matrices = args.skip_connectivity_matrices

base_dir = './'
results_dir = join(base_dir, 'res')
connectivity_dir = join(base_dir, 'connectivity')