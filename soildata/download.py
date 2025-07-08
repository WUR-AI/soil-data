import subprocess
import os

ISDA_PROPS = [
    'nitrogen_total', 'phosphorous_extractable', 'carbon_total', 
    'bulk_density', 'clay_content', 'sand_content', 'texture_class',
    'cation_exchange_capacity', 'ph'
]

def download_isda_rasters(rstdir:str, minx:float, miny:float, maxx:float, maxy:float):
    """
    Downloads the ISDA rasters for the given bounding box, and saves it in the
    given directory. It returns a dictionary mapping each soil property to its
    raster file.
    """
    module_path = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run([
        'bash', f'{module_path}/download_isda_rasters.bash',
        rstdir, str(minx), str(miny), str(maxx), str(maxy)
    ])
    assert result.returncode == 0
    # return os.listdir(rstdir)
    return {prop: f'{rstdir}/{prop}' for prop in ISDA_PROPS}