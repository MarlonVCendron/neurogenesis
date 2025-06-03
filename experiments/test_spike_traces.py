from brian2 import *
from utils.connect import Connect
from params.cells import cell_params
from plotting.voltage import plot_voltage
from params import cell_params, syn_params, ca3
from models.cells import (
    create_mgc,
    create_igc,
    create_bc,
    create_mc,
    create_hipp,
    create_pp,
    create_pca3,
    create_ica3,
)

seed(1)

defaultclock.dt = 0.1 * ms

def to_100(params):
  return {**params, "p": 1.0}

def main():
  start_scope()

  mgc  = create_mgc(N=1)
  igc  = create_igc(N=1)
  bc   = create_bc(N=1)
  mc   = create_mc(N=1)
  hipp = create_hipp(N=1)
  pca3 = create_pca3(N=1)
  ica3 = create_ica3(N=1)

  neurons = [mgc, igc, bc, mc, hipp, pca3, ica3]
  # neurons = [mgc]
  # neurons = [hipp]

  spike_monitors = [SpikeMonitor(neuron) for neuron in neurons]
  state_monitors = [StateMonitor(neuron, ['Vm'], record=True) for neuron in neurons]

  net = Network(collect())
  net.add(neurons)
  net.add(spike_monitors)
  net.add(state_monitors)

  def set_current(I):
    for neuron in neurons:
      neuron.I_ext = I

  set_current(0.0 * nA)
  net.run(50 * ms)

  set_current(0.5 * nA)
  net.run(200 * ms)

  set_current(1.0 * nA)
  net.run(200 * ms)

  set_current(0.0 * nA)
  net.run(100 * ms)

  set_current(-0.27 * nA)
  net.run(200 * ms)

  set_current(0.0 * nA)
  net.run(100 * ms)

  # set_current(0.75 * nA)
  # net.run(150 * ms)
  
  for neuron, spike_monitor, state_monitor in zip(neurons, spike_monitors, state_monitors):
    # plt.plot(state_monitor.t / ms, state_monitor.I_L[0] / nA)
    # plt.xticks(rotation=45)
    # plt.locator_params(axis="x", nbins=60)
    # plt.grid(True, which="both", linestyle="--", alpha=0.2)
    # plt.show()

    # plot_voltage(state_monitor, spike_monitor)
    plt.plot(state_monitor.t / ms, state_monitor.Vm[0] / mV, color="black")
    plt.xticks(rotation=45)
    plt.locator_params(axis="x", nbins=60)
    plt.grid(True, which="both", linestyle="--", alpha=0.2)
    plt.title(neuron.name)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.show()

if __name__ == '__main__':
  main()

