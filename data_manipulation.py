import logging
import osmnx as ox
import pandas as pd

def get_nodes_edges_from_graph(G, NUTS):
    """
    Creates the nodes and edges geo-dataframe for the network
    and adjust the geometry according to NUTS.
    """
    # Create nodes and edges representation
    logging.info("Creating nodes and edges representation")
    nodes, edges = ox.graph_to_gdfs(G)
    logging.info("Created")

    # Rebuilding Geometry
    logging.info("Rebuilding Geometries")
    edges.to_crs(NUTS.crs, inplace=True)
    nodes.to_crs(NUTS.crs, inplace=True)
    logging.info("Geometries built correctly")

    return nodes, edges

def create_output_dataframe(nrows, paths=5):
    """
    Create an empty dataframe properly formatted for the output
    """

    # Base Columns and dtypes
    columns = ["FROM", "TO", "FROM_NODE", "TO_NODE", "FROM_NAME", "TO_NAME"]
    types = {"FROM":float, "TO":float, "FROM_NODE":int, "TO_NODE":int, "FROM_NAME":str, "TO_NAME":str}

    # Create columns and types for any paths
    for path in range(1,paths+1):
        columns.append(f"PATH_{path}")
        types[f"PATH_{path}"] = object

    df = pd.DataFrame(columns=columns, index=range(0, nrows))
    df = df.astype(types)

    return df

