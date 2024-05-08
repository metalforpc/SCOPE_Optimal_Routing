import logging
import pickle
import geopandas as gpd

def load_network():
    """
    Load the Europe Network from Pickle file
    """
    logging.info("Loading Europe Network")

    with open("Europe_Graph.gpickle", "rb") as f:
        G = pickle.load(f)

    logging.info("Loaded")

    return G

def load_nuts(CODE_LEVEL = 0):
    """
    Load NUTS shapefile, default level is 0
    """
    
    # TODO Control that code level is INT

    logging.info("Loading NUTS Boundaries")

    df = gpd.read_file("Administrative_Boundaries/NUTS_RG_20M_2021_3035.shp")

    logging.info("Loaded")

    logging.info("Setting the NUTS level code")
    output = df[df.LEVL_CODE == CODE_LEVEL].copy().reset_index(drop=True)

    logging.info("Computing centroids")
    output.loc[:, 'centroids'] = output.centroid

    logging.info("Done")

    return output