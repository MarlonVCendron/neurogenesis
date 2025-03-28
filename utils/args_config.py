import argparse

parser = argparse.ArgumentParser(description="Hippocampal adult neurogenesis model")
parser.add_argument("--nmda", type=int, default=None, help="Scaling factor for NMDA")
parser.add_argument("--gaba", type=int, default=None, help="Scaling factor for GABA")
parser.add_argument("--ampa", type=int, default=None, help="Scaling factor for AMPA")
parser.add_argument("--trials", type=int, default=1, help="Number of trials")
parser.add_argument("--neurogenesis", action="store_true", help="Whether to include neurogenesis")
parser.add_argument("--single-run", action="store_true", help="Whether to run a single pattern only")

args = parser.parse_args()

