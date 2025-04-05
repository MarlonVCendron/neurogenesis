import argparse

parser = argparse.ArgumentParser(description="Hippocampal adult neurogenesis model")

parser.add_argument("--trials", type=int, default=1, help="Number of trials")

parser.add_argument("--nmda", type=float, default=None, help="Scaling factor for NMDA")
parser.add_argument("--gaba", type=float, default=None, help="Scaling factor for GABA")
parser.add_argument("--ampa", type=float, default=None, help="Scaling factor for AMPA")
parser.add_argument("--active-p", type=float, default=0.1, help="Percentage of active neurons in a pattern")
parser.add_argument("--igc-conn", type=float, default=1.0, help="IGC connectivity fraction (between 0 and 1)")
parser.add_argument("--break-time", type=float, default=300, help="Simulation time for the network to settle")
parser.add_argument("--stim-time", type=float, default=1000, help="Simulation time when activity is recorded")

parser.add_argument("--prefix", type=str, default=".", help="Prefix for the results directory")

parser.add_argument("--neurogenesis", action="store_true", help="Whether to include neurogenesis")
parser.add_argument("--ca3", action="store_true", help="Whether to include the CA3 in the model")
parser.add_argument("--single-run", action="store_true", help="Whether to run a single pattern only")
parser.add_argument("--skip-connectivity-matrices", action="store_true", help="Whether to skip the loading of connectivity matrices")
parser.add_argument("--generate-graph", action="store_true", help="Whether to generate the graph connectivity matrix")

parser.add_argument("--n-lamellae", type=int, default=20, help="Number of lamellae")
parser.add_argument("--n-pp", type=int, default=400, help="Number of PP axons")
parser.add_argument("--n-mgc", type=int, default=100, help="Number of mGC neurons per lamella")
parser.add_argument("--n-igc", type=int, default=10, help="Number of iMGC neurons per lamella")
parser.add_argument("--n-bc", type=int, default=1, help="Number of BC neurons per lamella")
parser.add_argument("--n-mc", type=int, default=4, help="Number of MC neurons per lamella")
parser.add_argument("--n-hipp", type=int, default=1, help="Number of HIPP neurons per lamella")
parser.add_argument("--n-pca3", type=int, default=30, help="Number of CA3 neurons per lamella")
parser.add_argument("--n-ica3", type=int, default=3, help="Number of ICA3 neurons per lamella")

args = parser.parse_args()

