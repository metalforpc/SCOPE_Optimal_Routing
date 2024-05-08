import osmnx as ox

def compute_optimal_route(G, NUTS, nodes, origin_node, country):
    dest_idx = nodes.geometry.sindex.nearest(NUTS[NUTS.NAME_LATN == country].centroids)[1][0]
    dest_node = nodes.iloc[dest_idx].name
    paths = ox.routing.k_shortest_paths(G, origin_node, dest_node, 5, weight="travel_time")
    paths = list(paths)
    return paths