import json 
import re
from src.request import get_access_token, get_layers_info, get_soil_data, get_soil_data_buffer
from src.utils import transform_crs, get_buffer_points
import geopandas as gpd
from tqdm import tqdm

with open('isda-credentials.json', 'r') as f:
    s = f.read()
    s = re.sub(r'\\(?![\\"bfnrt])', r'\\\\', s)
    credentials = json.loads(s)

access_token = get_access_token(credentials)
layers_info = get_layers_info(access_token)

soil_props = [
    'nitrogen_total', 'phosphorous_extractable', 'carbon_total', 
    'bulk_density', 'clay_content', 'sand_content', 'texture_class',
    'cation_exchange_capacity', 'ph'
]
depth = '0-20'

points = gpd.read_file('/mnt/c/Users/quint021/Documents/MBA Tanzania/points.geojson')
points = points.loc[points.mainharvestcrop == 'maize']

soil_data = {}

for idx, row in tqdm(list(points.iloc[274:].iterrows())):
    lon = row.geometry.x
    lat = row.geometry.y
    data_buffer = get_soil_data_buffer(
        lon=lon, lat=lat, soil_props=soil_props, buffer=50, crs='EPSG:32736', 
        access_token=access_token
    )
    data_str = json.dumps({idx: data_buffer})
    with open('soil-mbatza.txt', 'a') as f:
        f.write(data_str+'\n')
    # soil_data[idx] = data_buffer


# transform_crs(lon=522190.156, lat=8952742.721, crs_from='EPSG:32736')
# get_buffer_points(lon=522190.156, lat=8952742.721, crs='EPSG:32736', buffer=50)

# data_point =get_soil_data(
#     lon=36.203066, lat=-11.088261, soil_props=soil_props, 
#     access_token=access_token
# )

print()
