# Custom Test Cases and Analysis

This directory contains custom test cases for testing graph algorithms implementation in `tests/my_cases.jsonl`.

## 1. Test Cases Overview & Explanations

### Test 1: Ping
- **Input:** `{"task": "ping"}`
- **Expected Output:** `{"status": "ready"}`
- **Explanation:** Health check to verify that the service process is up and responding correctly.

### Test 2: DSU (Disjoint Set Union)
- **Input:** `{"task": "dsu", "n": 3, "operations": [[0, 1], [1, 2]]}`
- **Expected Output:** `{"states": [[2, 2], [1, 3]]}`
- **Explanation:**
  - Operation `[0, 1]`: Merges set containing 0 and 1. Resulting components count = 2, max set size = 2.
  - Operation `[1, 2]`: Merges set containing 1 and 2. All 3 elements are connected. Resulting components count = 1, max set size = 3.

### Test 3: Kruskal's Minimum Spanning Tree
- **Input:** `{"task": "kruskal", "n": 3, "edges": [[0, 1, 10], [1, 2, 5], [0, 2, 20]]}`
- **Expected Output:** `{"cost": 15, "edge_ids": [1, 0], "components": 1}`
- **Explanation:** Sorted edges by weight: edge 1 (weight 5), edge 0 (weight 10), edge 2 (weight 20). Kruskal selects edge 1 and edge 0. Total minimum cost = 15.

### Test 4: Prim's Minimum Spanning Tree
- **Input:** `{"task": "prim", "n": 3, "edges": [[0, 1, 10], [1, 2, 5], [0, 2, 20]]}`
- **Expected Output:** `{"cost": 15, "edge_ids": [1, 0], "components": 1}`
- **Explanation:** MST builds minimum spanning tree with weight 15 using edges 1 and 0, reaching all 3 vertices.

### Test 5: Strongly Connected Components (SCC)
- **Input:** `{"task": "scc", "n": 3, "edges": [[0, 1], [1, 2], [2, 0]]}`
- **Expected Output:** `{"component": [0, 0, 0], "condensation": []}`
- **Explanation:** Vertices 0, 1, and 2 form a single directed cycle, so they all belong to the same SCC (component 0). There are no cross-component edges.

### Test 6: Topological Sort
- **Input:** `{"task": "topo", "n": 3, "edges": [[0, 1], [1, 2]]}`
- **Expected Output:** `{"acyclic": true, "order": [0, 1, 2]}`
- **Explanation:** Directed line graph without cycles. Topological sorting yields `[0, 1, 2]`.

### Test 7: DAG Shortest Path
- **Input:** `{"task": "dag", "n": 3, "source": 0, "edges": [[0, 1, 5], [1, 2, 3], [0, 2, 10]]}`
- **Expected Output:** `{"acyclic": true, "distance": [0, 5, 8], "parent_edge": [-1, 0, 1]}`
- **Explanation:**
  - Shortest path from 0 to 1 is via edge 0 (cost 5).
  - Shortest path from 0 to 2 goes through vertex 1 (5 + 3 = 8) using edge 1, which is shorter than direct edge 2 (cost 10).

---

## 2. Direct Testing of `route_helper`

To test the `route_helper` function directly (as required by assignment guidelines), the following unit tests were executed in Python:

```python
from main import GraphAlgorithms

# Test route reconstruction for DAG
edges_map = {
    0: (0, 1, 5),
    1: (1, 2, 3),
    2: (0, 2, 10)
}
parent_edge = [-1, 0, 1]

# Path from source (0) to target (2)
path = GraphAlgorithms.route_helper(0, 2, parent_edge, edges_map)
assert path == [0, 1]  # Traverses edge 0 then edge 1

# Path from source (0) to source (0)
path_same = GraphAlgorithms.route_helper(0, 0, parent_edge, edges_map)
assert path_same == [0]
