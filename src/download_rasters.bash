#!/bin/bash

# ==============================================================================
# Download multiple remote raster files for a list of soil properties using a
# specified bounding box.
#
# Usage:
#   ./download_rasters.sh <dest_folder> <min_lon> <max_lat> <max_lon> <min_lat>
#
# Example:
#   ./download_rasters.sh /data/isda/ -5.7 43.5 -4.8 42.9
# ==============================================================================

if [ "$#" -ne 5 ]; then
    echo "Error: Invalid number of arguments."
    echo "Usage: $0 <dest_folder> <min_lon> <max_lat> <max_lon> <min_lat>"
    exit 1
fi

DST_FOLDER=$1
MIN_LON=$2
MAX_LAT=$3
MAX_LON=$4
MIN_LAT=$5

soil_props=(
    'nitrogen_total' 'phosphorous_extractable' 'carbon_total'
    'bulk_density' 'clay_content' 'sand_content' 'texture_class'
    'cation_exchange_capacity' 'ph'
)

echo "Starting batch raster crop for ${#soil_props[@]} properties..."
echo "Bounding Box (min_lon max_lat max_lon min_lat): $MIN_LON $MAX_LAT $MAX_LON $MIN_LAT"
echo "=================================================="

for PROP in "${soil_props[@]}"; do
    echo "Processing property: $PROP"

    SOURCE_URL="https://isdasoil.s3.amazonaws.com/soil_data/${PROP}/${PROP}.tif"
    VSI_SOURCE_URL="/vsicurl/${SOURCE_URL}"

    DST_FILENAME="${DST_FOLDER}/${PROP}.tif"

    echo "  -> Source: $SOURCE_URL"
    echo "  -> Output: $DST_FILENAME"

    gdal_translate "$VSI_SOURCE_URL" "$DST_FILENAME" \
        -projwin "$MIN_LON" "$MAX_LAT" "$MAX_LON" "$MIN_LAT" \
        -projwin_srs EPSG:4326
    wget https://isdasoil.s3.amazonaws.com/soil_data/${PROP}/${PROP}.json -O \
        ${DST_FOLDER}/${PROP}_metadata.json

    if [ $? -eq 0 ]; then
        echo "  -> Success!"
    else
        echo "  -> ERROR: gdal_translate failed for property '$PROP'."
    fi
    echo "--------------------------------------------------"
done

echo "Batch processing complete."