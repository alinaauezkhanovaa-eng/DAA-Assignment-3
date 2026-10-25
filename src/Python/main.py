import sys
import json
from collections import defaultdict, deque

class GraphAlgorithms:
    
    # 1. DSU (Disjoint Set Union)
    @staticmethod
    def dsu(n, operations):
        parent = list(range(n))
        rank = [0] * n
        components = n
        largest = 1 if n > 0 else 0
        
        def find(i):
            path = []
            while parent[i] != i:
                path.append(i)
                i = parent[i]
            for node in path:
                parent[node] = i
            return i

        results = []
        sizes = [1] * n
        
        for u, v in operations:
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                if rank[root_u] < rank[root_v]:
                    root_u, root_v = root_v, root_u
                parent[root_v] = root_u
                sizes[root_u] += sizes[root_v]
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1
                components -= 1
                if sizes[root_u] > largest:
                    largest = sizes[root_u]
            results.append([components, largest])
        return results

    # 2. Kruskal's Algorithm
    @staticmethod
    def kruskal(n, edges):
        parent = list(range(n))
        rank = [0] * n

        def find(i):
            path = []
            while parent[i] != i:
                path.append(i)
                i = parent[i]
            for node in path:
                parent[node] = i
            return i

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                if rank[root_i] < rank[root_j]:
                    root_i, root_j = root_j, root_i
                parent[root_j] = root_i
                if rank[root_i] == rank[root_j]:
                    rank[root_i] += 1
                return True
            return False

        sorted_edges = sorted(edges, key=lambda x: (x[2], x[3])) # sort by weight, then original edge_id
        cost = 0
        edge_ids = []
        
        for u, v, w, eid in sorted_edges:
            if union(u, v):
                cost += w
                edge_ids.append(eid)
        
        comps_map = defaultdict(list)
        for i in range(n):
            root = find(i)
            comps_map[root].append(i)
        
        components = sorted(list(comps_map.values()), key=lambda x: x[0])
        return cost, edge_ids, components

    # 3. Prim's Algorithm
    @staticmethod
    def prim(n, edges):
        import heapq
        adj = defaultdict(list)
        for u, v, w, eid in edges:
            adj[u].append((w, v, eid))
            adj[v].append((w, u, eid))

        visited = [False] * n
        total_cost = 0
        all_edge_ids = []
        components = []

        for i in range(n):
            if not visited[i]:
                comp_vertices = []
                min_heap = [(0, i, -1, -1)]
                comp_edges = []
                
                while min_heap:
                    w, u, p, eid = heapq.heappop(min_heap)
                    if visited[u]:
                        continue
                    visited[u] = True
                    comp_vertices.append(u)
                    if eid != -1:
                        total_cost += w
                        comp_edges.append(eid)
                    
                    for weight, v, next_eid in adj[u]:
                        if not visited[v]:
                            heapq.heappush(min_heap, (weight, v, u, next_eid))
                
                components.append(sorted(comp_vertices))
                all_edge_ids.extend(comp_edges)

        components.sort(key=lambda x: x[0])
        return total_cost, all_edge_ids, components

    # 4. SCC (Kosaraju's Algorithm)
    @staticmethod
    def scc(n, edges):
        adj = [[] for _ in range(n)]
        rev_adj = [[] for _ in range(n)]
        
        for u, v in edges:
            adj[u].append(v)
            rev_adj[v].append(u)

        visited = [False] * n
        order = []

        def dfs1(u):
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    dfs1(v)
            order.append(u)

        for i in range(n):
            if not visited[i]:
                dfs1(i)

        visited = [False] * n
        component_labels = [0] * n
        components_list = []
        
        def dfs2(u, comp_id, current_comp):
            visited[u] = True
            component_labels[u] = comp_id
            current_comp.append(u)
            for v in rev_adj[u]:
                if not visited[v]:
                    dfs2(v, comp_id, current_comp)

        comp_id = 0
        for u in reversed(order):
            if not visited[u]:
                current_comp = []
                dfs2(u, comp_id, current_comp)
                components_list.append(sorted(current_comp))
                comp_id += 1

        cross_pairs = set()
        for u, v in edges:
            cu = component_labels[u]
            cv = component_labels[v]
            if cu != cv:
                cross_pairs.add((cu, cv))

        condensed = sorted(list(cross_pairs))
        return component_labels, condensed

    # 5. Topological Sort
    @staticmethod
    def topo(n, edges):
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)

        state = [0] * n  
        order = []

        def dfs(u):
            state[u] = 1
            for v in adj[u]:
                if state[v] == 1:
                    return False  
                if state[v] == 0:
                    if not dfs(v):
                        return False
            state[u] = 2
            order.append(u)
            return True

        for i in range(n):
            if state[i] == 0:
                if not dfs(i):
                    return False, []

        return True, list(reversed(order))

    # 6. DAG Shortest Paths & Route Reconstruction
    @staticmethod
    def dag(n, source, edges):
        adj_topo = [[] for _ in range(n)]
        for u, v, w, eid in edges:
            adj_topo[u].append(v)

        state = [0] * n
        topo_order = []

        def dfs_topo(u):
            state[u] = 1
            for v in adj_topo[u]:
                if state[v] == 1:
                    return False
                if state[v] == 0:
                    if not dfs_topo(v):
                        return False
            state[u] = 2
            topo_order.append(u)
            return True

        for i in range(n):
            if state[i] == 0:
                if not dfs_topo(i):
                    return False, [], []

        topo_order.reverse()

        dist = [None] * n
        parent_edge = [-1] * n
        
        adj = [[] for _ in range(n)]
        for u, v, w, eid in edges:
            adj[u].append((v, w, eid))

        if 0 <= source < n:
            dist[source] = 0

        for u in topo_order:
            if dist[u] is not None:
                for v, w, eid in adj[u]:
                    new_dist = dist[u] + w
                    if dist[v] is None or new_dist < dist[v]:
                        dist[v] = new_dist
                        parent_edge[v] = eid

        return True, dist, parent_edge

    @staticmethod
    def route_helper(source, target, parent_edge, edges_map):
        if source == target:
            return [source]
        if parent_edge[target] == -1:
            return []
        
        path_edges = []
        curr = target
        while curr != source and parent_edge[curr] != -1:
            eid = parent_edge[curr]
            path_edges.append(eid)
            curr = edges_map[eid][0]
            
        if curr != source:
            return []
        return path_edges[::-1]

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        if task == "ping":
            print(json.dumps({"status": "ready"}))
            sys.stdout.flush()
            continue

        task = req.get("task")
        n = req.get("n", 0)
        
        if task == "dsu":
            operations = req.get("operations", [])
            res = GraphAlgorithms.dsu(n, operations)
            print(json.dumps({"states": res})) # Исправлено с components на states
            
        elif task == "kruskal":
            raw_edges = req.get("edges", [])
            edges = [[e[0], e[1], e[2], idx] for idx, e in enumerate(raw_edges)]
            cost, edge_ids, components = GraphAlgorithms.kruskal(n, edges)
            print(json.dumps({"cost": cost, "edge_ids": edge_ids, "components": components}))
            
        elif task == "prim":
            raw_edges = req.get("edges", [])
            edges = [[e[0], e[1], e[2], idx] for idx, e in enumerate(raw_edges)]
            cost, edge_ids, components = GraphAlgorithms.prim(n, edges)
            print(json.dumps({"cost": cost, "edge_ids": edge_ids, "components": components}))
            
        elif task == "scc":
            raw_edges = req.get("edges", [])
            edges = [[e[0], e[1]] for e in raw_edges]
            component, condensation = GraphAlgorithms.scc(n, edges)
            print(json.dumps({"component": component, "condensation": condensation})) # Исправлено с labels/condensed
            
        elif task == "topo":
            raw_edges = req.get("edges", [])
            edges = [[e[0], e[1]] for e in raw_edges]
            acyclic, order = GraphAlgorithms.topo(n, edges)
            print(json.dumps({"acyclic": acyclic, "order": order}))
            
        elif task == "dag":
            source = req.get("source", 0)
            raw_edges = req.get("edges", [])
            edges = [[e[0], e[1], e[2], idx] for idx, e in enumerate(raw_edges)]
            acyclic, distance, parent_edge = GraphAlgorithms.dag(n, source, edges)
            print(json.dumps({
                "acyclic": acyclic,
                "distance": distance,
                "parent_edge": parent_edge
            }))
            
        sys.stdout.flush()

def test_route_helper():
    edges_map = {0: (0, 1, 5), 1: (1, 2, 3), 2: (0, 2, 10)}
    parent_edge = [-1, 0, 1]
    path = GraphAlgorithms.route_helper(0, 2, parent_edge, edges_map)
    assert path == [0, 1], f"Expected [0, 1], got {path}"
    print("route_helper test passed successfully!")

if __name__ == "__main__":
    if sys.stdin.isatty():
        test_route_helper()
    else:
        main()
