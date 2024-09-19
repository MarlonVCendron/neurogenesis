import nest


def clusterConnectGenerator(cluster_index, n_clusters):
  def clusterConnect(from_pop, to_pop, syn_spec=None):
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
  return clusterConnect
