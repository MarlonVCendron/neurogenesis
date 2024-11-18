import nest
import csa

import models.cells.gc
import models.cells.bc
import models.cells.mc
import models.cells.hipp
from utils.connect import clusterConnectGenerator
from utils.debug import printConnections

N_clusters = 20
N_gcs = 2000  # Número de granule cells
N_bcs = 20  # Número de basket cells
N_mcs = 80  # Número de mossy cells
N_hipps = 40  # Número de HIPP cells

granule_cells = nest.Create("gc", N_gcs)
basket_cells = nest.Create("bc", N_bcs)
mossy_cells = nest.Create("mc", N_mcs)
hipp_cells = nest.Create("hipp", N_hipps)

def connectClusters(i, N_clusters):
  clusterConnect = clusterConnectGenerator(i, N_clusters)

  # Granule cells connections
  clusterConnect(granule_cells, basket_cells)
  clusterConnect(granule_cells, mossy_cells)
  clusterConnect(granule_cells, hipp_cells)

  # Basket cells connections
  clusterConnect(basket_cells, granule_cells)
  clusterConnect(basket_cells, mossy_cells)

  # Mossy cells connections
  clusterConnect(mossy_cells, granule_cells)
  clusterConnect(mossy_cells, basket_cells)
  clusterConnect(mossy_cells, hipp_cells)

  # HIPP cells connections
  clusterConnect(hipp_cells, granule_cells)
  clusterConnect(hipp_cells, basket_cells)
  clusterConnect(hipp_cells, mossy_cells)


def main():
  for i in range(N_clusters):
    connectClusters(i, N_clusters)

  print(nest.GetDefaults("static_synapse"))
  # print(nest.GetDefaults('iaf_cond_alpha_mc')['receptor_types'])
  # for x in nest.synapse_models:
  #   print(x)

  # connections = nest.GetConnections(granule_cells, basket_cells)
  # print(f"Total number of connections: {len(connections)}")
  
  # printConnections(granule_cells, target=True)
  # printConnections(granule_cells, target=False)
  # printConnections(basket_cells, target=True)
  # printConnections(basket_cells, target=False)
  
  printConnections(mossy_cells, target=True)
  printConnections(mossy_cells, target=False)



if __name__ == "__main__":
  main()
