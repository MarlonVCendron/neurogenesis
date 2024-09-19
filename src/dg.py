import nest
import csa

import models.cells.gc
import models.cells.bc
import models.cells.mc
import models.cells.hipp
from utils.connect import clusterConnect
from utils.debug import printConnections

N_clusters = 20
N_gcs = 2000  # Número de granule cells
N_bcs = N_clusters  # Número de basket cells
N_mcs = 80  # Número de mossy cells
N_hipps = 40  # Número de HIPP cells

granule_cells = nest.Create("gc", N_gcs)
basket_cells = nest.Create("bc", N_bcs)
mossy_cells = nest.Create("mc", N_mcs)
hipp_cells = nest.Create("hipp", N_hipps)

gcs_per_cluster = N_gcs // N_clusters
mcs_per_cluster = N_mcs // N_clusters
hipps_per_cluster = N_hipps // N_clusters

# Granule cells connections
for i in range(N_clusters):
  clusterConnect(granule_cells, basket_cells, N_clusters, i)
  clusterConnect(granule_cells, mossy_cells, N_clusters, i)
  clusterConnect(granule_cells, hipp_cells, N_clusters, i)

# Basket cells connections
for i in range(N_clusters):
  clusterConnect(basket_cells, granule_cells, N_clusters, i)
  clusterConnect(basket_cells, mossy_cells, N_clusters, i)
# nest.Connect(basket_cells, mossy_cells)

# Mossy cells connections
for i in range(N_clusters):
  clusterConnect(mossy_cells, granule_cells, N_clusters, i)
# nest.Connect(mossy_cells, basket_cells)
# nest.Connect(mossy_cells, hipp_cells)

# HIPP cells connections
for i in range(N_clusters):
  clusterConnect(hipp_cells, granule_cells, N_clusters, i)
# nest.Connect(hipp_cells, basket_cells)
# nest.Connect(hipp_cells, mossy_cells)


# connections = nest.GetConnections(granule_cells, basket_cells)
# print(f"Total number of connections: {len(connections)}")

# printConnections(granule_cells, target=True)
# printConnections(granule_cells, target=False)
# printConnections(basket_cells, target=True)
# printConnections(basket_cells, target=False)
