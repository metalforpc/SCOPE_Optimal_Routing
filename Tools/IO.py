import logging
import pickle
import geopandas as gpd
import itertools

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

    assert isinstance(CODE_LEVEL, int)

    # Load NUTS shapefile
    logging.info("Loading NUTS Boundaries")
    df = gpd.read_file("Administrative_Boundaries/NUTS_RG_20M_2021_3035.shp")
    logging.info("Loaded")

    # Setting the NUTS Level
    logging.info("Setting the NUTS level code")
    NUTS = df[df.LEVL_CODE == CODE_LEVEL].copy().reset_index(drop=True)

    # Compute centroids for each NUTS
    logging.info("Computing centroids")
    NUTS.loc[:, 'centroids'] = NUTS.centroid
    logging.info("Centroids computed")

    # Retrieve origins NUTS_ID
    logging.info("Retrieving origin and destination nuts")
    origins_nuts = NUTS.loc[(NUTS.CNTR_CODE == 'IT'), 'NUTS_ID'].unique()
    destinations_nuts = NUTS.loc[~(NUTS.CNTR_CODE == 'IT'), 'NUTS_ID'].unique()

    OD_names = list(itertools.product(origins_nuts, destinations_nuts))

    logging.info("Done")

    return NUTS, origins_nuts, destinations_nuts, OD_names