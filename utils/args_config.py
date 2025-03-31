import argparse

parser = argparse.ArgumentParser(description="Hippocampal adult neurogenesis model")
parser.add_argument("--nmda", type=int, default=None, help="Scaling factor for NMDA")
parser.add_argument("--gaba", type=int, default=None, help="Scaling factor for GABA")
parser.add_argument("--ampa", type=int, default=None, help="Scaling factor for AMPA")
parser.add_argument("--trials", type=int, default=1, help="Number of trials")
parser.add_argument("--active-p", type=float, default=0.1, help="Percentage of active neurons in a pattern")
parser.add_argument("--igc-conn", type=float, default=1.0, help="IGC connectivity fraction (between 0 and 1)")
parser.add_argument("--prefix", type=str, default="", help="Prefix for the results directory")
parser.add_argument("--neurogenesis", action="store_true", help="Whether to include neurogenesis")
parser.add_argument("--single-run", action="store_true", help="Whether to run a single pattern only")
parser.add_argument("--skip-connectivity-matrices", action="store_true", help="Whether to skip the loading of connectivity matrices")

args = parser.parse_args()

