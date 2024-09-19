import nest


def clusterConnect(from_pop, to_pop, n_clusters, cluster_index, syn_spec=None):
  from_per_cluster = len(from_pop) // n_clusters
  to_per_cluster = len(to_pop) // n_clusters
  from_index = cluster_index * from_per_cluster
  to_index = cluster_index * to_per_cluster

  nest.Connect(
      from_pop[from_index:from_index + from_per_cluster],
      to_pop[to_index:to_index + to_per_cluster],
      'all_to_all',
      syn_spec,
  )

# def clusterConnect(from_pop, to_pop, syn_spec=None):
#   len_from_pop = len(from_pop)
#   len_to_pop = len(to_pop)

#   if len_from_pop < len_to_pop:
#     if len_to_pop % len_from_pop != 0:
#       raise ValueError("The number of source cells must be a multiple of the number of target cells")

#     for i in range(len_from_pop):
#       nest.Connect(from_pop[i], to_pop[i::len_from_pop], 'all_to_all', syn_spec)
#   else:
#     if len_from_pop % len_to_pop != 0:
#       raise ValueError("The number of target cells must be a multiple of the number of source cells")

#     for i in range(len_to_pop):
#       nest.Connect(from_pop[i::len_to_pop], to_pop[i], 'all_to_all', syn_spec)
