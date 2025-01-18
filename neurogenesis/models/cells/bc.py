from brian2 import *
from neurogenesis.models.general.lif import LIF

params = {
    "Cm"        : 232.6 * pF,
    "g_L"       : 23.2 * nS,
    "E_L"       : -62.0 * mV,
    "g_ahp_max" : 76.9 * nS,
    "tau_ahp"   : 2.0 * ms,
    "E_ahp"     : -75.0 * mV,
    "V_th"      : -52.5 * mV,
    "I_ampa"    : -250 * pA,
    "I_nmda"    : 0 * pA,
    "I_gaba"    : 0 * pA,
}

lif_eqs = LIF()

bc = NeuronGroup(
    10,
    model      = lif_eqs,
    threshold  = 'Vm > V_th',
    reset      = 'Vm = E_L',
    method     = 'rk2',
    refractory = 0*ms          # A way to have lastspike
)
for param, value in params.items():
  setattr(bc, param, value)

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
