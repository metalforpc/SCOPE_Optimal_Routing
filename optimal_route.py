import osmnx as ox

def compute_optimal_route(G, NUTS, nodes, origin_node, country, k_paths = 5):

    dest_idx = nodes.geometry.sindex.nearest(NUTS[NUTS.CNTR_CODE == country].centroids)[1][0]
    print(dest_idx)
    dest_node = nodes.iloc[dest_idx].name
    
    paths = ox.routing.k_shortest_paths(G, origin_node, dest_node, k_paths, weight="travel_time")
    paths = list(paths)
    return paths