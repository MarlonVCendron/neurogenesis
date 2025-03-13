import h5py
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from py2cytoscape.data.cyrest_client import CyRestClient

from os.path import join
from params import results_dir
from params.cells import (
  N_mgc_l,
  N_igc_l,
  N_bc_l,
  N_mc_l,
  N_hipp_l
) 

cell_to_nl = {
  "bc": N_bc_l,
  "mc": N_mc_l,
  "mgc": N_mgc_l,
  "igc": N_igc_l,
  "hipp": N_hipp_l,
  "pp": 1
}


def export_to_gexf():
  h5_file_path = join(results_dir, "connectivity_matrices.h5")

  G = nx.DiGraph()
  with h5py.File(h5_file_path, 'r') as f:
    for group_name in f.keys():
      source_name, target_name = group_name.split("->")
      group = f[group_name]
      row = group["row"][:]
      col = group["col"][:]
      data = group["data"][:]
      for r, c, w in zip(row, col, data):
        source_node = f"{source_name}_{r}"
        target_node = f"{target_name}_{c}"

        if source_node not in G:
            attr_source = get_neuron_attributes(source_name, r)
            G.add_node(source_node, **attr_source)
        if target_node not in G:
            attr_target = get_neuron_attributes(target_name, c)
            G.add_node(target_node, **attr_target)
        
        G.add_edge(source_node, target_node)


  gephi_filename = join(results_dir, "network.gexf")
  nx.write_gexf(G, gephi_filename)

  cytoscape_filename = join(results_dir, "network_cytoscape.xml")
  nx.write_graphml(G, cytoscape_filename)

def get_neuron_attributes(cell, index):
  return {
    "cell": cell,
    "index": index,
    "lamella": index // cell_to_nl[cell],
  }


if __name__ == "__main__":
  export_to_gexf()
