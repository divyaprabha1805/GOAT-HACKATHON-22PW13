import heapq

def dijkstra(graph, start, goal, blocked_nodes=None, blocked_lanes=None):
    """
    Finds the shortest path from start to goal while avoiding blocked nodes and lanes.
    
    :param graph: NavGraph object containing vertices and edges.
    :param start: Start node ID.
    :param goal: Goal node ID.
    :param blocked_nodes: Set of blocked node IDs.
    :param blocked_lanes: Set of blocked lane tuples (start, end).
    :return: List of nodes representing the shortest path, or None if no path is found.
    """
    if blocked_nodes is None:
        blocked_nodes = set()
    if blocked_lanes is None:
        blocked_lanes = set()

    pq = []  # Priority queue for managing nodes to explore
    heapq.heappush(pq, (0, start))  # (cost, node)
    
    distances = {node: float('inf') for node in graph.vertices}  # Initialize distances
    distances[start] = 0
    
    previous_nodes = {node: None for node in graph.vertices}  # Track the shortest path
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node == goal:
            break  # Stop if we reach the destination
        
        if current_node in blocked_nodes:
            continue  # Skip nodes that are blocked

        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor in blocked_nodes or (current_node, neighbor) in blocked_lanes:
                continue  # Skip paths that are blocked

            distance = current_distance + weight
            
            if distance < distances[neighbor]:  # Update if a shorter path is found
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct the shortest path from goal to start
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    
    return path[::-1] if path and path[-1] == goal else None  # Return the path if valid
