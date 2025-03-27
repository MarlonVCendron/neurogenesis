import argparse

parser = argparse.ArgumentParser(description="Process some synaptic parameters.")
parser.add_argument("--nmda", type=int, default=None, help="Value for NMDA")
parser.add_argument("--gaba", type=int, default=None, help="Value for GABA")
parser.add_argument("--ampa", type=int, default=None, help="Value for AMPA")
parser.add_argument("--neurogenesis", type=bool, default=False, help="Whether to include neurogenesis")

args = parser.parse_args()

