""" This Scripts Compute the optimal routing for the whole europe."""

import numpy as np

import pandas as pd
import geopandas as gpd

import osmnx as ox
import networkx as nx

import IO
import data_manipulation
import optimal_route
import pickle

import logging
logging.getLogger().setLevel(logging.INFO)

import multiprocessing

if __name__ == "__main__":

    # Load Network from pickle file
    G = IO.load_network()

    # Load NUTS shapefile
    NUTS, origins_nuts, destinations_nuts = IO.load_nuts()

    # Get Nodes and Edges
    nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

    # Get OD nodes
    origin_nodes, destination_nodes, od_set = data_manipulation.od_nodes(origins_nuts, destinations_nuts, NUTS, nodes)

    # Define a function to run in parallel the optimal routings
    def parallel_route(destination_country):
        paths = optimal_route.compute_optimal_route(G, NUTS, nodes, origin_node, destination_country)
        return paths

    # Instantiate an array to save the results
    #output = data_manipulation.create_output_dataframe(country_list.shape[0])

    # Multicores optimal routing
    logging.info("Creating the pool")
    pool = multiprocessing.Pool(processes=country_list.shape[0])
    results = pool.map(parallel_route, iterable=country_list)

    # Close the pool to free up resources
    pool.close()
    pool.join()

    logging.info("Saving results to Pickle File")
    # Instantiate elements in the output array
    with open("res.pickle","wb") as f:
        pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)


    logging.warning("End of the script...")