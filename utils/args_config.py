import argparse

parser = argparse.ArgumentParser(description="Hippocampal adult neurogenesis model")

parser.add_argument("--trials", type=int, default=1, help="Number of trials")

parser.add_argument("--nmda", type=float, default=0.5, help="Scaling factor for NMDA")
parser.add_argument("--gaba", type=float, default=1.0, help="Scaling factor for GABA")
parser.add_argument("--ampa", type=float, default=1.0, help="Scaling factor for AMPA")
parser.add_argument("--tsodyks-scale", type=float, default=10.0, help="Scaling factor for tsodyks")
parser.add_argument("--active-p", type=float, default=0.1, help="Percentage of active neurons in a pattern")
parser.add_argument("--pp-rate", type=float, default=40, help="Rate of firing PP axons")
parser.add_argument("--igc-conn", type=float, default=1.0, help="IGC connectivity fraction (between 0 and 1)")
parser.add_argument("--break-time", type=float, default=500, help="Simulation time for the network to settle")
parser.add_argument("--stim-time", type=float, default=1000, help="Simulation time when activity is recorded")

parser.add_argument("--prefix", type=str, default=".", help="Prefix for the results directory")

parser.add_argument("--no-neurogenesis", action="store_true", help="Whether to exclude neurogenesis")
parser.add_argument("--no-ca3", action="store_true", help="Whether to exclude the CA3 in the model")
parser.add_argument("--single-run", action="store_true", help="Whether to run a single pattern only")
parser.add_argument("--skip-conn", action="store_true", help="Whether to skip the loading of connectivity matrices")
parser.add_argument("--generate-graph", action="store_true", help="Whether to generate the graph connectivity matrix")

parser.add_argument("--n-lamellae", type=int, default=20, help="Number of lamellae")
parser.add_argument("--n-pp", type=int, default=400, help="Number of PP axons")
parser.add_argument("--n-mgc", type=int, default=2000, help="Number of mGC neurons")
parser.add_argument("--n-igc", type=int, default=100, help="Number of iGC neurons")
parser.add_argument("--n-bc", type=int, default=120, help="Number of BC neurons")
parser.add_argument("--n-mc", type=int, default=100, help="Number of MC neurons")
parser.add_argument("--n-hipp", type=int, default=160, help="Number of HIPP neurons")
parser.add_argument("--n-pca3", type=int, default=600, help="Number of CA3 neurons")
parser.add_argument("--n-ica3", type=int, default=60, help="Number of ICA3 neurons")

args = parser.parse_args()

