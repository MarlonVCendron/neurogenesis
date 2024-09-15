import nest

import models.cells.gc
import models.cells.bc
import models.cells.mc
import models.cells.hipp

N_clusters = 20
N_gcs = 2000  # Número de granule cells
N_bcs = N_gcs//N_clusters  # Número de basket cells
N_mcs = 80  # Número de mossy cells
N_hipps = 40  # Número de HIPP cells

granule_cells = nest.Create("gc", N_gcs)
basket_cells = nest.Create("bc", N_bcs)
mossy_cells = nest.Create("mc", N_mcs)
hipp_cells = nest.Create("hipp", N_hipps)

# Granule cells connections
for i in range(N_bcs):
  nest.Connect(granule_cells[i::N_bcs], basket_cells[i])

# nest.Connect(granule_cells, mossy_cells)
# nest.Connect(granule_cells, hipp_cells)

# Basket cells connections
for i in range(N_bcs):
  nest.Connect(basket_cells[i], granule_cells[i::N_bcs])
# nest.Connect(basket_cells, mossy_cells)

# Mossy cells connections
# nest.Connect(mossy_cells, granule_cells)
# nest.Connect(mossy_cells, basket_cells)
# nest.Connect(mossy_cells, hipp_cells)

# HIPP cells connections
# nest.Connect(hipp_cells, granule_cells)
# nest.Connect(hipp_cells, basket_cells)
# nest.Connect(hipp_cells, mossy_cells)


connections = nest.GetConnections(granule_cells, basket_cells)

# Print number of connections
print(f"Total number of connections: {len(connections)}")

# Inspect a few connections (for example, the first 10 connections)
# for i, conn in enumerate(connections[:10]):
#     print(f"Connection {i + 1}: Source (GC) = {conn['source']}, Target (BC) = {conn['target']}")

# Verify the number of incoming connections per basket cell
for i, bc in enumerate(basket_cells[:10]):
  incoming = nest.GetConnections(target=bc)
  print(f"Basket cell {i + 1} has {len(incoming)} incoming connections")


for i, gc in enumerate(granule_cells[:10]):
  incoming = nest.GetConnections(source=gc)
  print(f"Granule cell {i + 1} has {len(incoming)} outgoing connections")
