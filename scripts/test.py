from brian2 import *

# Simulation parameters
duration = 1 * second  # Run for 1 second
N_pre = 8  # Number of active presynaptic neurons
rate = 40 * Hz  # Firing rate of each presynaptic neuron

# Neuron parameters
tau = 20 * ms  # Membrane time constant
V_rest = -70 * mV  # Resting potential
V_reset = -70 * mV  # Reset potential
V_th = -50 * mV  # Spiking threshold
R = 10 * Mohm  # Membrane resistance
EPSP = 0.2 * mV  # EPSP per spike

# Define neuron group
eqs = '''
dv/dt = (V_rest - v)/tau : volt
'''
G = NeuronGroup(1, eqs, threshold='v>V_th', reset='v=V_reset', method='exact')

# Synapses
P = PoissonGroup(N_pre, rates=rate)  # Active presynaptic neurons
S = Synapses(P, G, on_pre='v += EPSP')
S.connect()

# Monitor
M = SpikeMonitor(G)

# Run simulation
run(duration)

# Print result
print(f"Firing rate of the neuron in G2: {M.num_spikes / duration} Hz")
