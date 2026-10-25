# Algorithm Analysis & Technical Specification

## 1. Project Overview
This project implements a robust, high-performance graph processing engine designed to handle streaming JSON Lines requests via standard input/output (`stdin`/`stdout`). It covers six core graph algorithms alongside a protocol handshake (`ping`), adhering strictly to performance bounds, memory constraints, and strict schema contracts.

---

## 2. Core Components & Algorithmic Complexity

| Task | Algorithm Used | Time Complexity | Space Complexity | Key Design & Optimization Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`ping`** | Protocol Handshake | $O(1)$ | $O(1)$ | Instant response verifying system readiness (`{"status": "ready"}`). |
| **`dsu`** | Disjoint Set Union | $O(M \alpha(N))$ | $O(N)$ | Implemented with **Path Compression** and **Union by Rank/Size** to guarantee near-constant time per operation. Tracks component counts and largest set sizes dynamically. |
| **`kruskal`** | Minimum Spanning Tree | $O(E \log E)$ | $O(N + E)$ | Sorts edges by weight (and tie-breaking by original edge index), utilizing DSU for cycle detection. Supports 64-bit integer cost sums. |
| **`prim`** | Minimum Spanning Tree | $O(E \log V)$ | $O(N + E)$ | Uses an adjacency list paired with a binary min-heap (`heapq`) to greedily extract minimum weight crossing edges across all disconnected components. |
| **`scc`** | Kosaraju’s Algorithm | $O(V + E)$ | $O(V + E)$ | Two-pass DFS structure: first pass computes finish times on the original graph; second pass extracts strongly connected components on the transposed (reversed) graph. Builds condensed graph edges. |
| **`topo`** | Topological Sort | $O(V + E)$ | $O(V + E)$ | Three-state DFS recursion (`0 = unvisited`, `1 = visiting/recursion stack`, `2 = fully processed`) ensuring precise cycle detection and linear-time ordering. |
| **`dag`** | DAG Shortest Paths & Route Reconstruction | $O(V + E)$ | $O(V + E)$ | Combines topological sorting with dynamic programming edge relaxation. Reconstructs optimal routes back-to-source using parent edge pointers via `route_helper`. |

---

## 3. Robustness & Edge Cases Handled

* **Empty & Isolated Graphs:** Correctly handles $N = 0$, graphs with zero edges, or completely disconnected vertices without raising out-of-bounds or division-by-zero exceptions.
* **Self-Loops & Parallel Edges:** Safely filters or correctly computes weights and cycles when duplicate edges between the same vertex pair or single-vertex loops (`u == u`) are present.
* **Negative Weights & Cycles:** Properly identifies cycles in topological and DAG pipelines, returning safe fallback structures (`acyclic: false`, empty distance/parent lists) and handling negative edge weights in DAGs.
* **64-bit Integer Limits:** Native Python large integer handling ensures full compliance with massive edge-weight sums ($> 2^{31}-1$).
* **Stream Integrity:** Uses explicit `sys.stdout.flush()` after each JSON response line to prevent buffering bottlenecks during automated batch evaluation.

---

## 4. Route Reconstruction (`route_helper`)
The DAG module features a specialized route recovery utility (`route_helper`) that backtracks from a target vertex to a source vertex using stored parent edge identifiers:
* **Mechanism:** Iteratively traverses backwards from `target` using `parent_edge[curr]`, fetching the originating vertex from the corresponding edge map until `source` is reached.
* **Validation:** Returns an empty list `[]` if no valid path exists or if the path is broken by unreachable nodes (`distance is None`).
