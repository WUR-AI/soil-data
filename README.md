# Soils data

A set of scripts to download and process gridded soil data from global and regional databases.
The package can be installed with pip directly from this repo:

```
git clone https://github.com/WUR-AI/soil-data.git
cd soil-data
pip install -e .
```
Next datasets are included:
 
## [ISDASoil](https://www.isda-africa.com/isdasoil/)
 
It contains soil data at 30 m resolution for Africa at two soil layers (0-20cm and 20-50cm).
 
### Example usage
 
```python
from soildata.download import download_isda_raster
from soildata.utils import get_buffer_points

# Download the data for the fiven bounding box
bounding_box = gpd.read_file('data/geo/region-bounding-box.geojson')
minx, miny, maxx, maxy = bounding_box.to_crs(4326).total_bounds
rst_path, meta = download_isda_raster(RASTER_DIR, 'nitrogen_total', minx, miny, maxx, maxy)

# Extract the data for a all points in a geojson file
points = gpd.read_file('data/geo/points.geojson')
values = {i: {} for i in points.index}
rast = rio.open(rst_path)
points = points.to_crs(rast.crs)
band_names = [i['name'] for i in meta['assets']['image']['eo:bands']]
for idx, row in points.iterrows():
    # Get the coordinates of the points within a 50 m buffer. This is point itself
    # plus the 8 surrounding points (or pixels). Any buffer < res will return only 
    # the value of the point 
    buffer_points = list(
        get_buffer_points(row.geometry, buffer=50, res=30)
    )
    buffer_values = np.array(list(rast.sample(buffer_points)))
    # Estimate the average of all points within the buffer
    avg_values = buffer_values.mean(axis=0)
    values[idx].update({
        f'{band}': avg_values[i] 
        for i, band in enumerate(band_names)
    })
# Convert to a dataframe
values = pd.DataFrame.from_dict(values, orient='index')
```

## Soil-Grids