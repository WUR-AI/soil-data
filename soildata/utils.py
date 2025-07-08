from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import rasterio as rio

def transform_crs(lon:float, lat:float, crs_from:str, crs_to:str='EPSG:4326'):
    '''
    Transform a lat, lon pair from one crs to another.
    '''
    point = gpd.GeoSeries({'geometry': Point(lon, lat)}, crs=crs_from)
    point = point.to_crs(crs_to)
    return point.geometry.x.iloc[0], point.geometry.y.iloc[0]

def get_buffer_points(point:Point, buffer:float=30, res:float=30):
    '''
    Gets the soil data all the points centered in the area formed by the buffer on
    the point centered at lon, lat. The buffer is in meters, so lon, lat must be in
    a crs in meters.
    '''
    point_x, point_y = point.x, point.y

    ulcx = point_x - (buffer//res)*res
    ulcy = point_y + (buffer//res)*res
    points = np.meshgrid(
        [ulcx + i*res for i in range(2*(buffer//res) + 1)],
        [ulcy - i*res for i in range(2*(buffer//res) + 1)]
    )
    points = list(zip(points[0].flatten(), points[1].flatten()))
    points = filter( # Filter points within buffer distance
        lambda i: np.sqrt((i[0]-point_x)**2 + (i[1]-point_y)**2) <= buffer, 
        points
    )
    return list(points)



def get_data_on_points(points:gpd.GeoDataFrame, rst_dir:str, dataset:str='isda',
                       buffer:float=30, res:float=30):
    '''
    
    '''
    soil_props = PROPS[dataset]
    values = {}
    for prop in soil_props:
        rast = rio.open(f'/{rst_dir}/{prop}.tif')
        points = points.to_crs(rast.crs)
        values[prop] = {}
        for idx, row in points.iterrows():
            buffer_points = list(
                get_buffer_points(row.geometry, buffer=buffer, res=res)
            )
            values[prop][idx] = list(rast.sample(buffer_points))
        print(f'{prop} values extracted')
    return values

