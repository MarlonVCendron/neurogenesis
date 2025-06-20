import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy.sparse import csr_matrix
import networkx as nx
from utils.utils import read_connectivity
from os.path import join
from params import results_dir
from params.synapses import syn_params

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ConnectivityVisualizer:
    def __init__(self):
        self.cell_types = self._extract_cell_types()
        self.connections = self._extract_connections()
        self.conn_data = {}
        self._load_connectivity_data()
    
    def _extract_cell_types(self):
        """Extract all unique cell types from synapse definitions"""
        cell_types = set()
        for conn_name in syn_params.keys():
            source, target = conn_name.split('_', 1)
            cell_types.add(source)
            cell_types.add(target)
        return sorted(list(cell_types))
    
    def _extract_connections(self):
        """Extract all connections from synapse parameters"""
        connections = []
        for conn_name, params in syn_params.items():
            source, target = conn_name.split('_', 1)
            connections.append({
                'name': conn_name,
                'source': source,
                'target': target,
                'type': params['syn_type'],
                'probability': params.get('p', 0),
                'conductance': params.get('g', 0),
                'delay': params.get('delay', 0)
            })
        return connections
    
    def _load_connectivity_data(self):
        """Load actual connectivity data for each connection"""
        print("Loading connectivity data...")
        for conn in self.connections:
            try:
                conn_i, conn_j = read_connectivity(conn['source'], conn['target'])
                if len(conn_i) > 0:
                    shape = (max(conn_i) + 1, max(conn_j) + 1)
                    sparse_matrix = csr_matrix(
                        (np.ones(len(conn_i)), (conn_i, conn_j)), 
                        shape=shape
                    )
                    self.conn_data[conn['name']] = {
                        'matrix': sparse_matrix,
                        'shape': shape,
                        'n_connections': len(conn_i),
                        'conn_prob_from': np.mean(np.sum(sparse_matrix, axis=1)) / shape[1],
                        'conn_prob_to': np.mean(np.sum(sparse_matrix, axis=0)) / shape[0]
                    }
                else:
                    print(f"No connectivity data found for {conn['name']}")
            except Exception as e:
                print(f"Could not load connectivity for {conn['name']}: {e}")
    
    def plot_connectivity_matrix(self, figsize=(20, 10)):
        """Create a comprehensive connectivity matrix showing all connections"""
        n_types = len(self.cell_types)
        conn_matrix = np.zeros((n_types, n_types))
        type_to_idx = {cell_type: i for i, cell_type in enumerate(self.cell_types)}
        
        # Fill connectivity matrix
        for conn in self.connections:
            if conn['name'] in self.conn_data:
                source_idx = type_to_idx[conn['source']]
                target_idx = type_to_idx[conn['target']]
                # Use actual connection probability
                conn_matrix[source_idx, target_idx] = self.conn_data[conn['name']]['conn_prob_from']
        
        # Create the plot with reduced spacing
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        plt.subplots_adjust(wspace=0.3)  # Reduce space between subplots
        
        # Plot 1: Connection probability matrix
        im1 = ax1.imshow(conn_matrix, cmap='viridis', aspect='auto', interpolation='nearest')
        ax1.set_xticks(range(n_types))
        ax1.set_yticks(range(n_types))
        ax1.set_xticklabels(self.cell_types, rotation=45, ha='right', fontsize=12)
        ax1.set_yticklabels(self.cell_types, fontsize=12)
        ax1.set_xlabel('Target Cell Type', fontsize=14)
        ax1.set_ylabel('Source Cell Type', fontsize=14)
        ax1.set_title('Connection Probability Matrix', fontsize=16, pad=20)
        
        # Make colorbar smaller and better positioned
        cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8, aspect=20)
        cbar1.set_label('Connection Probability', fontsize=12)
        
        # Add text annotations with better visibility
        for i in range(n_types):
            for j in range(n_types):
                if conn_matrix[i, j] > 0:
                    # Choose text color based on background
                    text_color = 'white' if conn_matrix[i, j] > 0.5 else 'black'
                    ax1.text(j, i, f'{conn_matrix[i, j]:.3f}',
                            ha="center", va="center", color=text_color, 
                            fontsize=10, fontweight='bold')
        
        # Plot 2: Connection type matrix (excitatory/inhibitory)
        type_matrix = np.zeros((n_types, n_types))
        for conn in self.connections:
            if conn['name'] in self.conn_data:
                source_idx = type_to_idx[conn['source']]
                target_idx = type_to_idx[conn['target']]
                type_matrix[source_idx, target_idx] = 1 if conn['type'] == 'exc' else -1
        
        im2 = ax2.imshow(type_matrix, cmap='RdBu', vmin=-1, vmax=1, aspect='auto', interpolation='nearest')
        ax2.set_xticks(range(n_types))
        ax2.set_yticks(range(n_types))
        ax2.set_xticklabels(self.cell_types, rotation=45, ha='right', fontsize=12)
        ax2.set_yticklabels(self.cell_types, fontsize=12)
        ax2.set_xlabel('Target Cell Type', fontsize=14)
        ax2.set_ylabel('Source Cell Type', fontsize=14)
        ax2.set_title('Connection Type Matrix\n(Red=Excitatory, Blue=Inhibitory)', fontsize=16, pad=20)
        
        # Make colorbar smaller and better positioned
        cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8, aspect=20)
        cbar2.set_label('Connection Type', fontsize=12)
        cbar2.set_ticks([-1, 0, 1])
        cbar2.set_ticklabels(['Inhibitory', 'No Connection', 'Excitatory'])
        
        # Add text annotations for connection types
        for i in range(n_types):
            for j in range(n_types):
                if type_matrix[i, j] != 0:
                    text = 'E' if type_matrix[i, j] == 1 else 'I'
                    ax2.text(j, i, text, ha="center", va="center", 
                            color="white", fontsize=12, fontweight='bold')
        
        return fig
    
    def plot_network_graph(self, figsize=(15, 10)):
        """Create a network graph visualization"""
        G = nx.DiGraph()
        
        # Add nodes
        for cell_type in self.cell_types:
            G.add_node(cell_type)
        
        # Add edges with weights
        for conn in self.connections:
            if conn['name'] in self.conn_data:
                weight = self.conn_data[conn['name']]['conn_prob_from']
                color = 'red' if conn['type'] == 'exc' else 'blue'
                G.add_edge(conn['source'], conn['target'], 
                          weight=weight, color=color, conn_type=conn['type'])
        
        # Create layout
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                              node_size=3000, alpha=0.8, ax=ax)
        
        # Draw edges by type
        exc_edges = [(u, v) for u, v, d in G.edges(data=True) if d['conn_type'] == 'exc']
        inh_edges = [(u, v) for u, v, d in G.edges(data=True) if d['conn_type'] == 'inh']
        
        if exc_edges:
            exc_weights = [G[u][v]['weight'] * 10 for u, v in exc_edges]
            nx.draw_networkx_edges(G, pos, edgelist=exc_edges, edge_color='red',
                                 width=exc_weights, alpha=0.7, ax=ax, 
                                 connectionstyle="arc3,rad=0.1")
        
        if inh_edges:
            inh_weights = [G[u][v]['weight'] * 10 for u, v in inh_edges]
            nx.draw_networkx_edges(G, pos, edgelist=inh_edges, edge_color='blue',
                                 width=inh_weights, alpha=0.7, ax=ax,
                                 connectionstyle="arc3,rad=0.1")
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
        
        ax.set_title('Neural Network Connectivity Graph\n(Red=Excitatory, Blue=Inhibitory, Width=Connection Strength)')
        ax.axis('off')
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], color='red', lw=3, label='Excitatory'),
                          Line2D([0], [0], color='blue', lw=3, label='Inhibitory')]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return fig
    
    def plot_connection_details(self, figsize=(20, 15)):
        """Create detailed plots showing individual connection matrices"""
        n_connections = len([c for c in self.connections if c['name'] in self.conn_data])
        n_cols = 4
        n_rows = (n_connections + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_connections > 1 else [axes]
        
        plot_idx = 0
        for conn in self.connections:
            if conn['name'] in self.conn_data and plot_idx < len(axes):
                ax = axes[plot_idx]
                matrix = self.conn_data[conn['name']]['matrix']
                
                # Sample matrix if too large
                if matrix.shape[0] > 100 or matrix.shape[1] > 100:
                    sample_rows = np.random.choice(matrix.shape[0], min(100, matrix.shape[0]), replace=False)
                    sample_cols = np.random.choice(matrix.shape[1], min(100, matrix.shape[1]), replace=False)
                    sample_matrix = matrix[sample_rows, :][:, sample_cols]
                    title_suffix = " (sampled)"
                else:
                    sample_matrix = matrix
                    title_suffix = ""
                
                im = ax.imshow(sample_matrix.toarray(), cmap='Greys', 
                              aspect='auto', interpolation='nearest')
                
                color = 'red' if conn['type'] == 'exc' else 'blue'
                ax.set_title(f"{conn['name']}{title_suffix}\n"
                           f"P={conn['probability']:.3f}, "
                           f"Type={conn['type']}", 
                           color=color, fontsize=10)
                # ax.set_xlabel('Target neurons')
                # ax.set_ylabel('Source neurons')
                
                plot_idx += 1
        
        # Hide unused subplots
        for i in range(plot_idx, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        return fig
    
    def print_connectivity_stats(self):
        """Print comprehensive connectivity statistics"""
        print("\n" + "="*80)
        print("CONNECTIVITY STATISTICS")
        print("="*80)
        
        print(f"\nCell types: {', '.join(self.cell_types)}")
        print(f"Total connections defined: {len(self.connections)}")
        print(f"Connections with data: {len(self.conn_data)}")
        
        # Group by connection type
        exc_conns = [c for c in self.connections if c['type'] == 'exc']
        inh_conns = [c for c in self.connections if c['type'] == 'inh']
        
        print(f"\nExcitatory connections: {len(exc_conns)}")
        print(f"Inhibitory connections: {len(inh_conns)}")
        
        print(f"\n{'Connection':<15} {'Type':<4} {'P_def':<8} {'P_actual':<10} {'N_conn':<8} {'Shape':<12}")
        print("-" * 70)
        
        for conn in self.connections:
            if conn['name'] in self.conn_data:
                data = self.conn_data[conn['name']]
                print(f"{conn['name']:<15} {conn['type']:<4} "
                      f"{conn['probability']:<8.3f} {data['conn_prob_from']:<10.4f} "
                      f"{data['n_connections']:<8} {str(data['shape']):<12}")
        
        print("\n" + "="*80)
    
    def visualize_all(self, save_plots=False):
        """Create all visualizations"""
        print("Creating connectivity visualizations...")
        
        # Print statistics
        self.print_connectivity_stats()
        
        # Create plots
        fig1 = self.plot_connectivity_matrix()
        fig1.suptitle('Network Connectivity Overview', fontsize=16, y=0.98)
        
        fig2 = self.plot_network_graph()
        
        fig3 = self.plot_connection_details()
        fig3.suptitle('Individual Connection Matrices', fontsize=16, y=0.98)
        
        if save_plots:
            fig1.savefig(join(results_dir, 'connectivity_overview.png'), dpi=300, bbox_inches='tight')
            fig2.savefig(join(results_dir, 'connectivity_graph.png'), dpi=300, bbox_inches='tight')
            fig3.savefig(join(results_dir, 'connectivity_details.png'), dpi=300, bbox_inches='tight')
            print("Plots saved to results directory")
        
        plt.show()


if __name__ == "__main__":
    visualizer = ConnectivityVisualizer()
    visualizer.visualize_all(save_plots=True)
