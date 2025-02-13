from brian2 import *

has_igc    = False                    # Whether the network has immature GCs
N_lamellae = 20                       # Number of lamellae
igc_conn   = 1.0 if has_igc else 0.0  # IGC connection probability
ec_rate    = 40 * Hz                  # Rate of EC neurons