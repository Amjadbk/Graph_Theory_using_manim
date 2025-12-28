# Graph Theory Animations with Manim

A comprehensive collection of educational animations covering fundamental graph theory concepts, algorithms, and visualizations created using [Manim](https://www.manim.community/).

## 📚 Overview

This project provides animated visualizations for learning graph theory, including:

- **Graph Traversals**: BFS (Breadth-First Search) and DFS (Depth-First Search)
- **Shortest Path Algorithms**: Dijkstra's Algorithm
- **Eulerian Paths & Circuits**: Hierholzer's Algorithm and Fleury's Algorithm
- **Hamiltonian Paths & Cycles**: Backtracking algorithms and theorems
- **Graph Types**: Complete graphs, bipartite graphs, regular graphs, connected/disconnected graphs
- **Graph Representations**: Adjacency matrices, incidence matrices, adjacency lists, edge lists


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html)
- Required system dependencies (FFmpeg, LaTeX, etc.)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Amjadbk/Graph_Theory_using_manim.git
cd Graph_Theory_using_manim
```

2. Create a virtual environment (recommended):
```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

3. Install Manim and dependencies:
```bash
pip install manim
# Or if using conda:
conda install -c conda-forge manim
```

4. Install additional dependencies (if needed):
```bash
pip install numpy
```

### Running Animations

To render a specific animation:

```bash
# Render main graph sequence
manim -pql src/main.py GraphSequence

# Render BFS visualization
manim -pql src/bfs.py BFSQueueVisualization

# Render DFS visualization
manim -pql src/dfs.py DFSVisualization

# Render Dijkstra's algorithm
manim -pql src/dijkstra.py DijkstraVisualization

# Render Eulerian paths
manim -pql src/eulerian_path.py EulerianPaths

# Render Hamiltonian paths
manim -pql src/hamiltonian_path.py HamiltonConcepts
```

**Quality flags:**
- `-pql` or `--preview --quality low` - Low quality (480p15) for quick preview
- `-pqm` or `--preview --quality medium` - Medium quality (720p30)
- `-pqh` or `--preview --quality high` - High quality (1080p60)


## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new graph theory concepts
- Improve existing animations
- Fix bugs or enhance performance
- Add more examples or use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Manim Community](https://www.manim.community/) for the amazing animation engine
- Graph theory community for educational resources

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This project is designed for educational purposes. The animations are suitable for teaching graph theory concepts in classrooms, online courses, or self-study.

