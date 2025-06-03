from brian2 import *
import numpy as np
from utils.args_config import args

from params import break_time, stim_time
from utils.patterns import get_population_pattern, get_pattern_per_lamella
from utils.utils import neuron_ordering


def plot_state_monitors(state_monitors, save=True, filename="?"):
    if state_monitors is None or len(state_monitors) == 0:
        return
        
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

    state_monitors = sorted(state_monitors, key=lambda sm: neuron_ordering.index(sm.source.name))

    plt.figure(figsize=(20, len(state_monitors) * 4))

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    for idx, state_mon in enumerate(state_monitors):
        neuron = state_mon.source

        ax1 = plt.subplot(len(state_monitors), 1, idx + 1)

        # Plot each synaptic current with a different color
        currents_to_plot = [
            state_mon.Vm[0],
            state_mon.I[0],
            state_mon.U[0],
            state_mon.I_syn_1[0],
            state_mon.I_syn_2[0],
            state_mon.I_syn_3[0],
            state_mon.I_syn_4[0],
            state_mon.I_syn_5[0]
        ]
        labels = ["Vm", "I", "U", "I_syn_1", "I_syn_2", "I_syn_3", "I_syn_4", "I_syn_5"]

        for i, current in enumerate(currents_to_plot):
            ax1.plot(state_mon.t / ms, current, marker='o', color=colors[i % len(colors)], markersize=1, linestyle='None')

        ax1.legend(labels)
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel(neuron.name)
        ax1.set_xlim(break_time / ms, (break_time + stim_time) / ms)
    if save:
        plt.savefig(f"figures/state_monitors/{filename}.png")
        plt.close()
    else:
        plt.show()
