""" This Scripts Compute the optimal routing for the whole europe"""

import numpy as np

import pandas as pd
import geopandas as gpd

import osmnx as ox
import networkx as nx

import IO
import data_manipulation
import optimal_route

import logging
logging.setLevel(logging.DEBUG)

import multiprocessing

if __name__ == "__main__":
    # Load Network from pickle file
    G = IO.load_network()

    # Load NUTS shapefile
    NUTS = IO.load_nuts()

    # Get Nodes and Edges
    nodes, edges = data_manipulation.get_nodes_edges_from_graph()

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

    # Allocate cores
    with multiprocessing.Pool(len(country_list)) as pool:
        logging.info("Starting optimal routing")
        res = pool.map(parallel_route, country_list)
        pool.close()
        pool.join()

    logging.warning("End of the script...")