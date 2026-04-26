import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random


class DeadlockDetector:
    """Detects deadlocks in a resource allocation graph using cycle detection."""
    
    @staticmethod
    def detect_deadlock(graph):
        """
        Detects if there is a cycle in the directed graph.
        A cycle indicates a deadlock in resource allocation.
        
        Args:
            graph: networkx DiGraph object
            
        Returns:
            tuple: (has_deadlock: bool, cycles: list of lists)
        """
        try:
            cycles = list(nx.simple_cycles(graph))
            has_deadlock = len(cycles) > 0
            return has_deadlock, cycles
        except:
            return False, []


class DeadlockDetectorGUI:
    """GUI for deadlock detection with graph visualization."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Algorithm")
        self.root.geometry("1000x700")
        
        self.graph = None
        self.pos = None
        self.detector = DeadlockDetector()
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas for graph
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.randomize_btn = tk.Button(
            button_frame,
            text="Randomize Graph",
            command=self.randomize_graph,
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=10,
            font=("Arial", 11, "bold")
        )
        self.randomize_btn.pack(side=tk.LEFT, padx=5)
        
        self.detect_btn = tk.Button(
            button_frame,
            text="Detect Deadlock",
            command=self.detect_deadlock,
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=10,
            font=("Arial", 11, "bold")
        )
        self.detect_btn.pack(side=tk.LEFT, padx=5)
        
        # Create status label
        self.status_label = tk.Label(
            main_frame,
            text="Status: Ready",
            font=("Arial", 10),
            fg="#555"
        )
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Initialize with random graph
        self.randomize_graph()
    
    def generate_random_graph(self, num_nodes=6, edge_probability=0.3):
        """
        Generate a random directed graph representing resource allocation.
        
        Args:
            num_nodes: Number of nodes in the graph (even number for P and R pairs)
            edge_probability: Probability of edge between process and resource (0-1)
            
        Returns:
            networkx DiGraph object
        """
        graph = nx.DiGraph()
        
        # Ensure even number of nodes (half processes, half resources)
        if num_nodes % 2 != 0:
            num_nodes += 1
        
        num_processes = num_nodes // 2
        num_resources = num_nodes // 2
        
        # Add process nodes
        processes = [f"P{i}" for i in range(num_processes)]
        for p in processes:
            graph.add_node(p, type="P")
        
        # Add resource nodes
        resources = [f"R{i}" for i in range(num_resources)]
        for r in resources:
            graph.add_node(r, type="R")
        
        # Add edges: Process -> Resource (request) and Resource -> Process (allocation)
        for process in processes:
            # Each process requests 1-2 resources
            num_requests = random.randint(1, 2)
            requested_resources = random.sample(resources, min(num_requests, len(resources)))
            for resource in requested_resources:
                if random.random() < edge_probability:
                    graph.add_edge(process, resource)
        
        for resource in resources:
            # Each resource is allocated to 0-2 processes
            num_allocations = random.randint(0, 2)
            allocated_processes = random.sample(processes, min(num_allocations, len(processes)))
            for process in allocated_processes:
                if random.random() < edge_probability:
                    graph.add_edge(resource, process)
        
        return graph
    
    def draw_graph(self, graph, highlight_cycles=None):
        """
        Draw the graph on the canvas.
        
        Args:
            graph: networkx DiGraph object
            highlight_cycles: List of cycles to highlight in red
        """
        self.ax.clear()
        
        if graph.number_of_nodes() == 0:
            self.ax.text(0.5, 0.5, "No graph to display", 
                        ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        # Use spring layout for better visualization
        self.pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
        
        # Draw all edges
        nx.draw_networkx_edges(
            graph, self.pos,
            ax=self.ax,
            edge_color="#888",
            arrows=True,
            arrowsize=20,
            arrowstyle="->",
            width=2,
            connectionstyle="arc3,rad=0.1"
        )
        
        # Draw process nodes (circles)
        process_nodes = [node for node in graph.nodes() if graph.nodes[node].get('type') == 'P']
        nx.draw_networkx_nodes(
            graph, self.pos,
            nodelist=process_nodes,
            ax=self.ax,
            node_color='#FF9800',  # Orange
            node_size=1500,
            alpha=0.9,
            node_shape='o'  # Circle
        )
        
        # Draw resource nodes (squares)
        resource_nodes = [node for node in graph.nodes() if graph.nodes[node].get('type') == 'R']
        nx.draw_networkx_nodes(
            graph, self.pos,
            nodelist=resource_nodes,
            ax=self.ax,
            node_color='#9C27B0',  # Purple
            node_size=1500,
            alpha=0.9,
            node_shape='s'  # Square
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            graph, self.pos,
            ax=self.ax,
            font_size=10,
            font_weight='bold',
            font_color='white'
        )
        
        # Highlight cycles if provided
        if highlight_cycles:
            for cycle in highlight_cycles:
                cycle_edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
                nx.draw_networkx_edges(
                    graph, self.pos,
                    edgelist=cycle_edges,
                    ax=self.ax,
                    edge_color='red',
                    arrows=True,
                    arrowsize=20,
                    arrowstyle="->",
                    width=3,
                    connectionstyle="arc3,rad=0.1"
                )
        
        self.ax.set_title("Resource Allocation Graph\n(Orange = Process, Purple = Resource)", 
                         fontsize=12, fontweight='bold')
        self.ax.axis('off')
        self.canvas.draw()
    
    def randomize_graph(self):
        """Generate and display a new random graph."""
        self.graph = self.generate_random_graph(
            num_nodes=random.randint(6, 10),
            edge_probability=random.uniform(0.2, 0.5)
        )
        self.draw_graph(self.graph)
        self.status_label.config(text="Status: Graph randomized", fg="#4CAF50")
    
    def detect_deadlock(self):
        """Detect and display deadlocks in the current graph."""
        if self.graph is None or self.graph.number_of_nodes() == 0:
            messagebox.showwarning("Warning", "No graph to analyze. Please randomize first.")
            return
        
        has_deadlock, cycles = self.detector.detect_deadlock(self.graph)
        
        # Redraw with cycles highlighted
        self.draw_graph(self.graph, highlight_cycles=cycles if has_deadlock else None)
        
        if has_deadlock:
            cycle_info = "\n".join([f"Cycle {i+1}: {' → '.join(cycle)} → {cycle[0]}" 
                                   for i, cycle in enumerate(cycles)])
            message = f"DEADLOCK DETECTED!\n\n{len(cycles)} cycle(s) found:\n\n{cycle_info}"
            self.status_label.config(text=f"Status: DEADLOCK DETECTED ({len(cycles)} cycle(s))", 
                                     fg="#F44336")
            messagebox.showwarning("Deadlock Detected", message)
        else:
            message = "No deadlock detected! The system is safe."
            self.status_label.config(text="Status: No deadlock - System is safe", fg="#4CAF50")
            messagebox.showinfo("Safe System", message)


def main():
    root = tk.Tk()
    app = DeadlockDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
