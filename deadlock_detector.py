import tkinter as tk # python's gui lbrary
from tkinter import messagebox # popup dialouges
import networkx as nx # graph library to work with nodes, edges, and detect cytcles 
import matplotlib.pyplot as plt # plotting library for drawing graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #integrate matplotlib graphs into tkinter windows
from matplotlib.figure import Figure
import random # used to generate random graphs 


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
            cycles = list(nx.simple_cycles(graph)) #NetworkX find all cycles in a graph 
            has_deadlock = len(cycles) > 0 # if there are any cycles, then we have a deadlock
            return has_deadlock, cycles #retursn true/false and list of cycles found
        except:
            return False, []

# GUI code
class DeadlockDetectorGUI:
    """GUI for deadlock detection with graph visualization."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Algorithm")
        self.root.geometry("1000x700")
        
        self.graph = None #start with no graph
        self.pos = None #store node positions
        self.detector = DeadlockDetector() #createas an instance of the deadlock detector
        
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
            command=self.randomize_graph, #calls the main algorithm to detect deadlocks
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
            command=self.detect_deadlock, #calls the main algorithm to detect deadlocks
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
        Intentionally creates complex deadlock cycles for educational purposes.
        
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
        processes = [f"P{i}" for i in range(num_processes)] #list of all processes
        for p in processes:
            graph.add_node(p, type="P")
        
        # Add resource nodes
        resources = [f"R{i}" for i in range(num_resources)] #list of all resources
        for r in resources:
            graph.add_node(r, type="R")
        
        # CREATE INTENTIONAL DEADLOCK CYCLE
        # Example: P0 → R0 → P1 → R1 → P2 → R0 (creates cycle)
        cycle_length = random.randint(3, min(num_processes, num_resources))
        for i in range(cycle_length):
            process = processes[i % num_processes]
            resource = resources[i % num_resources]
            next_process = processes[(i + 1) % num_processes]
            
            # P_i requests R_i
            graph.add_edge(process, resource)
            # R_i is allocated to P_{i+1}
            graph.add_edge(resource, next_process)
        
        # Add some additional random edges for complexity
        for process in processes:
            # Each process may request 1-2 additional random resources
            if random.random() < 0.6:
                num_extra_requests = random.randint(1, 2)
                extra_resources = random.sample(resources, min(num_extra_requests, len(resources)))
                for resource in extra_resources:
                    if not graph.has_edge(process, resource):  # Avoid duplicates
                        if random.random() < edge_probability:
                            graph.add_edge(process, resource)
        
        for resource in resources:
            # Each resource may be allocated to 1 additional process
            if random.random() < 0.5:
                additional_process = random.choice(processes)
                if not graph.has_edge(resource, additional_process):  # Avoid duplicates
                    graph.add_edge(resource, additional_process)
        
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
            edge_probability=random.uniform(0.3, 0.6)
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
