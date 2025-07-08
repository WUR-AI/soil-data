import requests
from pyproj import Transformer
import rasterio as rio
import os

logf = print # In case I want to change the logging function

ISDA_PROPS = [
    'nitrogen_total', 'phosphorous_extractable', 'carbon_total', 
    'bulk_density', 'clay_content', 'sand_content', 'texture_class',
    'cation_exchange_capacity', 'ph', 'bedrock_depth', 'aluminium_extractable',
    'calcium_extractable', 'carbon_organic', 'fcc', 'iron_extractable', 
    'magnesium_extractable', 'phosphorous_extractable', 'potassium_extractable',
    'silt_content', 'stone_content', 'sulphur_extractable', 'zinc_extractable',
]
ISDA_URL_BASE = 'https://isdasoil.s3.amazonaws.com/soil_data'

def download_isda_raster(rstdir:str, prop:str, minx:float, miny:float, maxx:float, 
                          maxy:float):
    """
    Downloads the ISDA rasters for the given bounding box, and saves it in the
    given directory. It returns the path to the downloaded raster, and a dict
    containing the metadata.

    Parameters
    -----------
    rstdir: str
        The directory to save the rasters in.
    prop: str
        Soil property to download. One in:
            'nitrogen_total', 'phosphorous_extractable', 'carbon_total', 
            'bulk_density', 'clay_content', 'sand_content', 'texture_class',
            'cation_exchange_capacity', 'ph', 'bedrock_depth', 'aluminium_extractable',
            'calcium_extractable', 'carbon_organic', 'fcc', 'iron_extractable', 
            'magnesium_extractable', 'phosphorous_extractable', 'potassium_extractable',
            'silt_content', 'stone_content', 'sulphur_extractable', 'zinc_extractable',
    minx, miny, maxx, maxy: float
        The bounding box to download the rasters for.
    """
    file_location = f'{ISDA_URL_BASE}/{prop}/{prop}.tif'
    rst_name = f'{rstdir}/{prop}.tif'
    if not os.path.exists(rst_name):
        with rio.open(file_location) as file:
            transformer = Transformer.from_crs("epsg:4326", file.crs)
            # convert the data from lat/lon to x,y coords of the source dataset crs
            start_coords = transformer.transform(maxy, minx)
            end_coords = transformer.transform(miny, maxx)
            # get the location of the pixel at the given location (in lon/lat (x/y) order))
            start_coords= file.index(start_coords[0], start_coords[1])
            end_coords=file.index(end_coords[0], end_coords[1])
            
            window = rio.windows.Window(
                start_coords[1], start_coords[0], end_coords[1] - start_coords[1], 
                end_coords[0] - start_coords[0]
            )
            logf(f'Downloading {prop}...')
            arr = file.read(window=window)
            new_profile = file.profile.copy()

        new_profile.update({
                'height': window.height,
                'width': window.width,
                'count': file.count,
                'transform': file.window_transform(window)
        })
        with rio.open(rst_name, 'w', **new_profile) as dst:
            dst.write(arr)
        logf(f'{rst_name} created.')
    else:
        logf(f'{rst_name} already exists, skipping...')

    response = requests.get(f'https://isdasoil.s3.amazonaws.com/soil_data/{prop}/{prop}.json')
    
    return rst_name, response.json()