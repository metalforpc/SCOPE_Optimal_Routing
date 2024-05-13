""" This Scripts Compute the optimal routing for the whole europe."""

import numpy as np

import pandas as pd
import geopandas as gpd

import osmnx as ox
import networkx as nx

from Routines import IO, data_manipulation, optimal_route
import pickle

import logging
logging.getLogger().setLevel(logging.INFO)

import multiprocessing

if __name__ == "__main__":

    # Load Network from pickle file
    G = IO.load_network()

    # Load NUTS shapefile
    NUTS, origins_nuts, destinations_nuts, OD_names = IO.load_nuts()

    # Get Nodes and Edges
    nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

    # Get OD nodes
    origin_nodes, destination_nodes, od_set = data_manipulation.od_nodes(origins_nuts, destinations_nuts, NUTS, nodes)

    # Define a function to run in parallel the optimal routings
    def parallel_route(OD):
        paths = optimal_route.compute_single_dijkstra(G, OD)
        return paths

    # Instantiate an array to save the results
    output_df = data_manipulation.create_output_dataframe_2(len(od_set))

    # Multicores optimal routing
    logging.info("Creating the pool")
    pool = multiprocessing.Pool(processes=len(od_set))
    results = pool.map(parallel_route, iterable=od_set)

    # Close the pool to free up resources
    pool.close()
    pool.join()

    # Unpack results

    # Instantiate elements in the output array
    with open("res.pickle","wb") as f:
        pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    data_manipulation.unpack_results_to_df(results, output_df, OD_names)
    output_df.to_csv("NUTS0.csv", index=False)


    logging.warning("End of the script...")