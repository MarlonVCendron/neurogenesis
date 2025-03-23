import numpy as np
import matplotlib.pyplot as plt

directory = "/home/marlon/edu/mestrado/proj/Chavlis_Hippocampus_2017/3dendrites/ConnectivityMatrices_3dendrites/"
file_path = directory + "syn_eg1.txt"
data = np.load(file_path, allow_pickle=True)

presynaptic = data["presynaptic"]
postsynaptic = data["postsynaptic"]

print("Presynaptic neurons:", presynaptic)
print("Postsynaptic neurons:", postsynaptic)

# num_neurons = max(presynaptic.max(), postsynaptic.max()) + 1  # Infer number of neurons
# connectivity_matrix = np.zeros((num_neurons, num_neurons))

connectivity_matrix = np.zeros((presynaptic.max() + 1, postsynaptic.max() + 1))

# Fill the matrix (rows = presynaptic, columns = postsynaptic)
for pre, post in zip(presynaptic, postsynaptic):
    connectivity_matrix[pre, post] = 1

print(np.sum(connectivity_matrix, axis=1))

# Plot the connectivity matrix
plt.imshow(connectivity_matrix, cmap="Greys", origin="lower")
plt.xlabel("Postsynaptic Neuron")
plt.ylabel("Presynaptic Neuron")
plt.title("Connectivity Matrix")
plt.show()


total_connections = len(presynaptic)
unique_presynaptic = len(np.unique(presynaptic))
unique_postsynaptic = len(np.unique(postsynaptic))
average_connections = total_connections / unique_presynaptic if unique_presynaptic > 0 else 0

print(f"Total connections: {total_connections}")
print(f"Unique presynaptic neurons: {unique_presynaptic}")
print(f"Unique postsynaptic neurons: {unique_postsynaptic}")
print(f"Average connections per presynaptic neuron: {average_connections:.2f}")
