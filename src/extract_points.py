'''
It gets the soil data from the iSDA soil rasters. Samples the raster all the points
around the buffer of each point in a geodataframe.

It saves the sampled values in a dict, where the for each variable, the key is the
index of the geodataframe.
'''
import geopandas as gpd
from utils import get_buffer_points
import rasterio as rio
import pickle


points = gpd.read_file('/mnt/c/Users/quint021/Documents/MBA Tanzania/points.geojson')
DATA_DIR = '/data/isda-soils/files/mba-tza'

soil_props = [
    'nitrogen_total', 'phosphorous_extractable', 'carbon_total', 
    'bulk_density', 'clay_content', 'sand_content', 'texture_class',
    'cation_exchange_capacity', 'ph'
]

values = {}
for prop in soil_props:
    rast = rio.open(f'/{DATA_DIR}/{prop}.tif')
    points = points.to_crs(rast.crs)
    values[prop] = {}
    for idx, row in points.iterrows():
        buffer_points = list(get_buffer_points(row.geometry, buffer=50, res=30))
        values[prop][idx] = list(rast.sample(buffer_points))
    print(f'{prop} values extracted')

with open(f'{DATA_DIR}/soil_props_points.pickle', 'wb') as f:
    pickle.dump(values, f)