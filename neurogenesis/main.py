from brian2 import *
from models.general import LIF

start_scope()


lif = NeuronGroup(1, eqs, method='exact')

run(100*ms)