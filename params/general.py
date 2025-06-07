from brian2 import *
from os.path import join

from utils.args_config import args

# Number of trials
trials = 1 if args.single_run else args.trials

# Percentage of active neurons in a pattern
active_p = args.active_p

# Whether the network has immature GCs
has_igc = not args.no_neurogenesis

# Number of lamellae
N_lamellae = args.n_lamellae

# IGC connectivity fraction
igc_conn = args.igc_conn if has_igc else 0.0

has_ca3 = not args.no_ca3

# Rate of EC neurons
pp_rate = 40 * Hz

# Simulation time for the network to settle
break_time = args.break_time * ms
# Simulation time when activity is recorded
stim_time = args.stim_time * ms

# Whether to skip the loading of connectivity matrices
skip_connectivity_matrices = args.skip_connectivity_matrices

base_dir = './'
results_dir = join(base_dir, 'res')
connectivity_dir = join(base_dir, 'connectivity')
latex_dir = join(base_dir, 'thesis')