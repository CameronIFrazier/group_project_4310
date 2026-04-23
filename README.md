# Deadlock Detection Algorithm with GUI

A visual deadlock detection system that analyzes resource allocation graphs and identifies deadlocks through cycle detection.

## Features

- **Visual Graph Representation**: Displays a resource allocation graph with:
  - Orange nodes = Processes (P)
  - Purple nodes = Resources (R)
  - Directed edges showing resource requests/allocations

- **Deadlock Detection**: Uses cycle detection algorithm to identify deadlocks
  - Highlights deadlock cycles in red
  - Shows detailed cycle information
  
- **Interactive GUI**:
  - **Randomize Graph**: Generate a new random resource allocation graph
  - **Detect Deadlock**: Analyze the current graph for deadlocks

## How It Works

The deadlock detector uses **cycle detection** in a directed graph:
- Each process-to-resource edge represents a resource request
- Each resource-to-process edge represents a resource allocation
- A cycle indicates a deadlock (circular wait condition)

## Installation

### Requirements
```
Python 3.7+
networkx
matplotlib
tkinter (usually included with Python)
```

### Setup
```bash
pip install networkx matplotlib
```

## Usage

Run the application:
```bash
python deadlock_detector.py
```

### GUI Controls

1. **Randomize Graph Button** (Green)
   - Generates a new random resource allocation graph
   - Clears any previous deadlock detection results
   - Uses random graph size (6-8 nodes) and edge probability

2. **Detect Deadlock Button** (Blue)
   - Analyzes the current graph for cycles
   - Highlights deadlock cycles in red
   - Shows detailed information about detected deadlocks

3. **Status Label**
   - Displays current system status
   - Shows number of cycles if deadlock detected

## Algorithm Details

### Cycle Detection Algorithm
The application uses NetworkX's `simple_cycles()` function which implements Donald B. Johnson's algorithm:
- Time Complexity: O((N + E)(C + 1)) where N = nodes, E = edges, C = number of cycles
- Space Complexity: O(N + E)

### Deadlock Conditions Met
A deadlock occurs when all four Coffman conditions are met:
1. **Mutual Exclusion**: Resources cannot be shared (represented by single allocation)
2. **Hold and Wait**: Processes hold resources while requesting others
3. **No Preemption**: Resources cannot be forcibly taken
4. **Circular Wait**: Cycle in the resource allocation graph

This system detects condition #4 (Circular Wait).

## Example

1. Click "Randomize Graph" to create a new graph
2. Click "Detect Deadlock" to analyze it
3. If deadlock is found, the cycle will be highlighted in red
4. A message box shows the exact deadlock cycle

## File Structure

```
deadlock_detection/
├── deadlock_detector.py    # Main application
└── README.md              # This file
```

## Notes

- The graph layout is randomized for each visualization using spring layout
- Edge probability affects how many connections exist in the graph
- Smaller graphs (more sparse) are less likely to have deadlocks
- Denser graphs increase the probability of deadlock occurrence
