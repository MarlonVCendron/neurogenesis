from brian2 import *
from neurogenesis.models.general.lif import LIF

lif_eqs = LIF()
bc = NeuronGroup(
    1,
    model=lif_eqs,
    threshold='Vm > V_th',
    reset='Vm = E_L',
    method='euler',
    refractory=0*ms  # A way to have lastspike
)
bc.Cm        = 232.6 * pF
bc.g_L       = 23.2 * nS
bc.E_L       = -62.0 * mV
bc.g_ahp_max = 76.9 * nS
bc.tau_ahp   = 2 * ms
bc.E_ahp     = -75.0 * mV
bc.V_th      = -52.5 * mV
bc.I_syn     = -250 * pA

bc.Vm = bc.E_L

state_mon = StateMonitor(bc, 'Vm', record=True)
spike_mon = SpikeMonitor(bc)

run(100*ms)

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
