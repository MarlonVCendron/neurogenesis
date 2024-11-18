from brian2 import *

start_scope()

eqs = '''
  dv/dt = I_leak / Cm : volt
  I_leak = g_L*(E_L - v) : amp
'''

G = NeuronGroup(1, eqs, method='exact')

run(100*ms)