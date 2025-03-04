import h5py
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from os.path import join
from params import results_dir


filename = join(results_dir, "connectivity_matrices.h5")


def load_and_visualize_groups():
  group_keys = []
  with h5py.File(filename, 'r') as f:
    group_keys = list(f.keys())

  G = nx.DiGraph()

  for key in group_keys:
    try:
      source, target = key.split("->")
    except ValueError:
      print(f"Unexpected group name format: {key}")
      continue

    # Add an edge from the source group to the target group
    G.add_edge(source, target)

  # Draw the graph using a spring layout
  plt.figure(figsize=(8, 6))
  pos = nx.spring_layout(G, seed=42)
  nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightgreen",
          edge_color="gray", arrowsize=20, font_size=10)
  plt.title("Connectivity Graph: Population Groups")
  plt.show()


def abbreviate(pop_name):
    # Define a mapping if available; otherwise, default to first two lowercase letters.
  mapping = {
      "pyramidal": "pp",
      "granule": "gc",
      "basket": "bc"
  }
  pop_name_lower = pop_name.lower()
  for key, abbr in mapping.items():
    if key in pop_name_lower:
      return abbr
  return pop_name_lower[:2]


def visualize_grouped_connectivity():
  G = nx.DiGraph()

  with h5py.File(filename, 'r') as f:
    # Iterate over each connectivity group in the file.
    for group_name in f.keys():
      try:
        source, target = group_name.split("->")
      except ValueError:
        print(f"Skipping group with unexpected format: {group_name}")
        continue

      # Abbreviate population names.
      source_abbr = abbreviate(source)
      target_abbr = abbreviate(target)

      # Load the connection data from the group.
      group = f[group_name]
      # Number of connections is given by the length of the 'data' dataset.
      num_connections = group["data"].shape[0]

      # Add nodes if not already present.
      if source_abbr not in G:
        G.add_node(source_abbr)
      if target_abbr not in G:
        G.add_node(target_abbr)

      # If an edge already exists, sum the connection weights.
      if G.has_edge(source_abbr, target_abbr):
        G[source_abbr][target_abbr]['weight'] += num_connections
      else:
        G.add_edge(source_abbr, target_abbr, weight=num_connections)

  # Draw the aggregated connectivity graph.
  plt.figure(figsize=(8, 6))
  pos = nx.spring_layout(G, seed=42)
  nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue',
          arrowsize=20, font_size=12)

  # Optionally, draw edge labels to show connection weights.
  edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

  plt.title("Aggregated Connectivity Graph")
  plt.show()


def load_full_connectivity_graph():
  """
  Loads all connectivity groups from the HDF5 file and constructs a directed graph
  where each node represents an individual cell. Nodes are named as 'pop_index' (e.g., 'pp_0').
  """
  G = nx.DiGraph()
  nodes_added = set()

  with h5py.File(filename, 'r') as f:
    for group_name in f.keys():
      try:
        source, target = group_name.split("->")
      except ValueError:
        print(f"Skipping group with unexpected format: {group_name}")
        continue

      src_abbr = abbreviate(source)
      tgt_abbr = abbreviate(target)
      group = f[group_name]
      shape = group.attrs["shape"]
      n_source, n_target = shape

      # Add all source nodes (if not already added)
      for i in range(n_source):
        src_node = f"{src_abbr}_{i}"
        if src_node not in nodes_added:
          G.add_node(src_node, population=src_abbr)
          nodes_added.add(src_node)
      # Add all target nodes
      for j in range(n_target):
        tgt_node = f"{tgt_abbr}_{j}"
        if tgt_node not in nodes_added:
          G.add_node(tgt_node, population=tgt_abbr)
          nodes_added.add(tgt_node)

      # Add edges from connectivity data
      rows = group["row"][:]
      cols = group["col"][:]
      for r, c in zip(rows, cols):
        src_node = f"{src_abbr}_{r}"
        tgt_node = f"{tgt_abbr}_{c}"
        if G.has_edge(src_node, tgt_node):
          G[src_node][tgt_node]['weight'] += 1
        else:
          G.add_edge(src_node, tgt_node, weight=1)
  return G


def assign_initial_positions(G):
  """
  Assigns an initial position for each node by clustering nodes of the same population
  together. Each population gets a "center" on a circle, and individual cells get a small
  random offset around that center.
  """
  # Group nodes by their population
  populations = {}
  for node, data in G.nodes(data=True):
    pop = data.get('population', '')
    populations.setdefault(pop, []).append(node)

  num_pops = len(populations)
  angle_step = 2 * np.pi / num_pops
  centers = {}
  cluster_radius = 10  # distance from the origin for cluster centers
  for i, pop in enumerate(populations.keys()):
    angle = i * angle_step
    centers[pop] = np.array([cluster_radius * np.cos(angle), cluster_radius * np.sin(angle)])

  # For each node, assign a position: center of its population + small random offset.
  initial_pos = {}
  np.random.seed(42)
  for pop, nodes in populations.items():
    center = centers[pop]
    for node in nodes:
      offset = np.random.normal(scale=1.0, size=2)
      initial_pos[node] = center + offset
  return initial_pos


def visualize_full_connectivity():
  """
  Constructs the full connectivity graph from the HDF5 file and visualizes it.
  All cells are shown as individual nodes labeled by their population abbreviations.
  Nodes from the same population are initialized close together, and the spring layout
  refines the positions so that connected cells tend to cluster.
  """
  G = load_full_connectivity_graph()
  init_pos = assign_initial_positions(G)
  # Run a spring layout starting from the initial positions to help connected nodes cluster.
  pos = nx.spring_layout(G, pos=init_pos, iterations=100, seed=42)

  # Create labels (simply the population abbreviation for each node)
  labels = {node: data['population'] for node, data in G.nodes(data=True)}

  plt.figure(figsize=(12, 10))
  nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
  nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=10, edge_color='gray')
  nx.draw_networkx_labels(G, pos, labels, font_size=8)

  plt.title("Full Connectivity Graph with Cell Clustering")
  plt.axis('off')
  plt.show()


if __name__ == '__main__':
  visualize_full_connectivity()
