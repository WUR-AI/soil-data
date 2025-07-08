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

    It returns a list of (x, y) pairs.
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

