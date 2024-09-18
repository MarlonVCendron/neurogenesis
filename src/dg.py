import nest
import csa

import models.cells.gc
import models.cells.bc
import models.cells.mc
import models.cells.hipp
from utils.connect import clusterConnect

N_clusters = 20
N_gcs = 2000  # Número de granule cells
N_bcs = N_clusters  # Número de basket cells
N_mcs = 80  # Número de mossy cells
N_hipps = 40  # Número de HIPP cells

granule_cells = nest.Create("gc", N_gcs)
basket_cells = nest.Create("bc", N_bcs)
mossy_cells = nest.Create("mc", N_mcs)
hipp_cells = nest.Create("hipp", N_hipps)

# Granule cells connections
clusterConnect(granule_cells, basket_cells)
# nest.Connect(granule_cells, basket_cells)
# nest.Connect(granule_cells, mossy_cells)
# nest.Connect(granule_cells, hipp_cells)

# Basket cells connections
clusterConnect(basket_cells, granule_cells)
# nest.Connect(basket_cells, mossy_cells)

# Mossy cells connections
# nest.Connect(mossy_cells, granule_cells)
# nest.Connect(mossy_cells, basket_cells)
# nest.Connect(mossy_cells, hipp_cells)

# HIPP cells connections
# nest.Connect(hipp_cells, granule_cells)
# nest.Connect(hipp_cells, basket_cells)
# nest.Connect(hipp_cells, mossy_cells)


# connections = nest.GetConnections(granule_cells, basket_cells)
# print(f"Total number of connections: {len(connections)}")

for i, bc in enumerate(basket_cells[:10]):
  incoming = nest.GetConnections(target=bc)
  print(f"Basket cell {i + 1} has {len(incoming)} incoming connections")

for i, gc in enumerate(granule_cells[:10]):
  incoming = nest.GetConnections(source=gc)
  print(f"Granule cell {i + 1} has {len(incoming)} outgoing connections")
