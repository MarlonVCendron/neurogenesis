from brian2 import *

Cm        = 232.6 * pF  # Membrane capacitance
g_L       = 23.2 * nS   # Leak conductance
E_L       = -62.0 * mV  # Leak reversal potential
g_ahp_max = 76.9 * nS   # Maximum AHP conductance
tau_ahp   = 2 * ms      # AHP time constant
E_ahp     = -75.0 * mV  # AHP reversal potential
V_th      = -52.5 * mV  # Threshold potential

eq = Equations('''
  dVm/dt = (-I_L -I_ahp -I_syn) / Cm                    : volt
  I_L    = g_L * (Vm - E_L)                             : amp
  I_ahp  = g_ahp * (Vm - E_ahp)                         : amp
  g_ahp  = g_ahp_max * e ** (- (t - t_spike) / tau_ahp) : siemens
  I_syn  = 0                                            : amp
''')

lif = NeuronGroup(1, model=eq, threshold='Vm > V_th', reset='Vm = E_L')
lif.Vm = E_L

# Record
spike_mon = SpikeMonitor(lif)
state_mon = StateMonitor(lif, 'Vm', record=True)

run(100 * ms)

# Plot
figure(figsize=(12, 4))
subplot(121)
plot(state_mon.t / ms, state_mon.Vm[0] / mV)
xlabel('Time (ms)')
ylabel('Membrane potential (mV)')
subplot(122)
plot(spike_mon.t / ms, spike_mon.i, '|k')
xlabel('Time (ms)')
ylabel('Neuron index')
tight_layout
show()
