""" This Scripts Compute the optimal routing for the whole europe"""

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
    NUTS = IO.load_nuts()

    # Get Nodes and Edges
    nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

    # Get list of countries
    country_list = NUTS.CNTR_CODE.unique()
    country_list = country_list[~(country_list == 'IT')]

    # For each pair ("IT", country) compute the optimal route
    # Among all nodes, find the nearest to a given centroid

    # Instantiate origin node ("IT")
    origin_idx = nodes.geometry.sindex.nearest(NUTS[NUTS.CNTR_CODE == "IT"].centroids)[1][0]
    origin_node = nodes.iloc[origin_idx].name

    # Define a function to run in parallel the optimal routings
    def parallel_route(destination_country):
        paths = optimal_route.compute_optimal_route(G, NUTS, nodes, origin_node, destination_country)

    # Instantiate an array to save the results
    #output = data_manipulation.create_output_dataframe(country_list.shape[0])

    # Multicores optimal routing
    pool = multiprocessing.Pool(processes=country_list.shape[0])
    results = [pool.apply_async(parallel_route, (country,)) for country in country_list]
    final_results = [result.get() for result in results]

    # Close the pool to free up resources
    pool.close()
    pool.join()

    logging.info("Saving results to Pickle File")
    # Instantiate elements in the output array
    with open("res.pickle","wb") as f:
        pickle.dump(final_results, f, protocol=pickle.HIGHEST_PROTOCOL)


    logging.warning("End of the script...")