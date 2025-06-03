from brian2 import *
from terminology import in_red

from models.general import synapse, synapse_tsodyks
from utils.utils import read_connectivity
from utils.args_config import args

def connect_synapses(synapses, p, condition):
    source = synapses.source
    target = synapses.target

    # Connect either via connectivity matrix or randomly
    conn_i, conn_j = read_connectivity(source, target)

    try:
        if len(conn_i) > 0 and len(conn_j) > 0:
            synapses.connect(i=conn_i, j=conn_j)
        else:
            # This will randomly connect the synapses, even for the same source and target, but different receptors
            synapses.connect(p=p, condition=condition)
    except Exception as e:
        message = "🐙 Error connecting synapses, probably because you changed the connection without changing the connectivity matrix"
        print(in_red(message))
        print(e)


def legacy(source, target, receptor, delay, g_max, tau_r, tau_d, p=1, condition=None):
    (eqs, on_pre) = synapse(receptor)

    synapses = Synapses(
        source=source,
        target=target,
        model=eqs,
        on_pre=on_pre,
        delay=delay,
        method="rk4",
    )

    connect_synapses(synapses, p, condition)

    synapses.g_max = g_max
    synapses.tau_r = tau_r
    synapses.tau_d = tau_d

    return synapses


def tsodyks(source, target, syn_type, syn_var, delay, g, tau_r, tau_d, tau_f, U_se, p=1, condition=None):
    (eqs, on_pre) = synapse_tsodyks(syn_type, syn_var)

    synapses = Synapses(
        source=source,
        target=target,
        model=eqs,
        on_pre=on_pre,
        delay=delay,
        method="rk4",
    )

    connect_synapses(synapses, p, condition)

    synapses.g = g
    synapses.tau_r = tau_r
    synapses.tau_d = tau_d
    synapses.tau_f = tau_f
    synapses.U_se = U_se
    synapses.scale = args.tsodyks_scale

    return synapses


def Connect(*args, **kwargs):
    if kwargs.get("U_se"):
        synapses = tsodyks(*args, **kwargs)
    else:
        synapses = legacy(*args, **kwargs)

    return synapses
