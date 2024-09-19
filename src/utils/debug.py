import nest


def printConnections(pop, target=True, n=10):
  for i, cell in enumerate(pop[:n]):
    connections = nest.GetConnections(target=cell) if target else nest.GetConnections(source=cell)
    connection_type = 'incoming' if target else 'outgoing'
    print(f"{cell.get('model')} {i + 1} has {len(connections)} {connection_type} connections")
