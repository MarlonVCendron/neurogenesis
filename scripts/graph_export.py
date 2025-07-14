import h5py
import networkx as nx
import numpy as np
from math import pi

from os.path import join
from params import results_dir
from params.cells import (
  N_mgc_l,
  N_igc_l,
  N_bc_l,
  N_pca3_l,
  N_ica3_l,
  N_hipp_l,
  N_mc_l,
  N_pp,
  N_mgc,
  N_igc,
  N_bc,
  N_pca3,
  N_ica3,
  N_hipp,
  N_mc,
) 
from params.general import N_lamellae

cell_to_nl = {
  "bc": N_bc_l,
  "mgc": N_mgc_l,
  "igc": N_igc_l,
  "pca3": N_pca3_l,
  "ica3": N_ica3_l,
  "mc": N_mc_l,
  "hipp": N_hipp_l,
  "pp": 1
}

cell_polygon = {
    "pp": 4,
    "mgc": 0,
    "igc": 0,
    "bc": 3,
    "mc":6,
    "hipp": 0,
    "pca3": 3,
    "ica3": 0,
}

CELL_TOTALS = {
    "pp": N_pp, "mgc": N_mgc, "igc": N_igc, "bc": N_bc,
    "hipp": N_hipp, "mc": N_mc, "pca3": N_pca3, "ica3": N_ica3,
}

LAYOUT_CONFIG = {
    'ica3': {'layers': 1, 'spacing_before': 30},
    'pca3': {'layers': 5, 'spacing_before': 10},
    'hipp': {'layers': 1, 'spacing_before': 20},
    'mc':   {'layers': 1, 'spacing_before': 5},
    'bc':   {'layers': 1, 'spacing_before': 5},
    'igc':  {'layers': 1, 'spacing_before': 20},
    'mgc':  {'layers': 6, 'spacing_before': 10},
    'pp':   {'layers': 1, 'spacing_before': 30},
}

CELL_ORDER = ['ica3', 'pca3', 'hipp', 'mc', 'bc', 'igc', 'mgc', 'pp']

def calculate_radii():
    radii = {}
    current_radius = 0
    layer_spacing = 10

    for cell_type in CELL_ORDER:
        conf = LAYOUT_CONFIG[cell_type]
        num_layers = conf['layers']
        
        current_radius += conf['spacing_before']
        
        cell_radii = []
        for i in range(num_layers):
            cell_radii.append(current_radius)
            current_radius += layer_spacing

        radii[cell_type] = cell_radii
        
    return radii

CELL_RADII = calculate_radii()


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

        # weight = w
        # if (source_name, target_name) in {
        #     ("pp", "mgc"),
        #     ("pp", "igc"),
        #     ("mgc", "pca3"),
        #     ("igc", "ica3"),
        #     ("pca3", "pca3"),
        #     ("ica3", "pca3"),
        #     ("pca3", "ica3"),
        # }:
        #     weight = 10
        # G.add_edge(source_node, target_node, weight=weight)

        G.add_edge(source_node, target_node)


  gephi_filename = join(results_dir, "network.gexf")
  nx.write_gexf(G, gephi_filename)
  print(f"Exported to {gephi_filename}")

  cytoscape_filename = join(results_dir, "network_cytoscape.xml")
  nx.write_graphml(G, cytoscape_filename)
  print(f"Exported to {cytoscape_filename}")

  try:
    tulip_filename = join(results_dir, "network_tulip.dot")
    nx.drawing.nx_pydot.write_dot(G, tulip_filename)
    print(f"Exported to {tulip_filename} (for Tulip)")
  except ImportError:
    print("\nSkipping DOT export for Tulip. To enable it, install pydot and graphviz.")

def get_neuron_attributes(cell, index):
    total_neurons = CELL_TOTALS[cell]
    num_layers = LAYOUT_CONFIG[cell]['layers']
    radii = CELL_RADII[cell]

    neurons_per_layer = (total_neurons + num_layers - 1) // num_layers
    
    layer_index = index // neurons_per_layer
    index_in_layer = index % neurons_per_layer
    
    if layer_index >= len(radii):
        layer_index = len(radii) - 1
    
    radius = radii[layer_index]
    
    lamella = index // cell_to_nl.get(cell, 1)

    if cell in ['mgc', 'igc', 'bc', 'mc', 'pca3', 'ica3']:
        num_lamellae = N_lamellae
        angle_per_lamella = 2 * pi / num_lamellae
        lamella_angle_start = lamella * angle_per_lamella

        if cell in ['pca3', 'ica3']:
            lamella_spacing_fraction = 0.0
        else:
            lamella_spacing_fraction = 0.2
        
        angle_spread = angle_per_lamella * (1 - lamella_spacing_fraction)

        if cell in ['mgc', 'pca3']:
            neurons_per_lamella = cell_to_nl.get(cell, 1)
            index_in_lamella = index % neurons_per_lamella

            mgc_layer_index = index_in_lamella % num_layers
            radius = radii[mgc_layer_index]

            neurons_per_spot = (neurons_per_lamella + num_layers - 1) // num_layers
            position_in_spot = index_in_lamella // num_layers
            
            if neurons_per_spot > 1:
                angle_offset = (position_in_spot / (neurons_per_spot - 1)) * angle_spread
            else:
                angle_offset = angle_spread / 2
            
            angle = lamella_angle_start + angle_offset
        else: # igc, bc, mc, ica3
            neurons_per_lamella = cell_to_nl.get(cell, 1)
            index_in_lamella = index % neurons_per_lamella
            
            if neurons_per_lamella > 1:
                angle_offset = (index_in_lamella / (neurons_per_lamella - 1)) * angle_spread
            else:
                angle_offset = angle_spread / 2

            angle = lamella_angle_start + angle_offset
    else: # pp, hipp
        if layer_index == num_layers - 1:
            neurons_in_this_layer = total_neurons - (layer_index * neurons_per_layer)
        else:
            neurons_in_this_layer = neurons_per_layer
        angle = (index_in_layer / neurons_in_this_layer) * 2 * pi

    if num_layers > 1 and cell != 'mgc':
        angle += (np.random.rand() - 0.5) * 0.1 / num_layers

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    return {
        "cell": cell,
        "index": index,
        "lamella": lamella,
        "x": x,
        "y": y,
        "Polygon": cell_polygon[cell],
    }


if __name__ == "__main__":
  export_to_gexf()
