import sentinel_api as s3api
from datetime import datetime
from osgeo import ogr
from user_data import DownloadParams, Paths


def copernicus_download():
    """
    This function takes the user input specified in user_data.py to create a API call for the Copernicus Hub and
    downloads the specified data.
    """
    start_time = datetime.now()

    ############## Sentinel Download ##############

    # Set Sentinel api
    s1 = s3api.SentinelDownloader(DownloadParams.username, DownloadParams.password, DownloadParams.api_url)

    # Set download directory
    s1.set_download_dir(Paths.download_dir)

    # Set bounding box for area of investigation
    polygon = get_extent(shapefile=Paths.shapefile_dir)
    print(polygon)
    s1.set_geometries(polygon)

    # Search for corresponding data scenes via api
    s1.search(DownloadParams.satellite, DownloadParams.min_overlap, Paths.download_dir, DownloadParams.start_date,
              DownloadParams.end_date, producttype=DownloadParams.product)

    # Download data - returns dictionary of downloaded data scenes
    # (Format: {'failed': ['', '', ..], 'success': ['', '', '', ..]})
    s1.download_all()

    download_time = datetime.now()
    print("Copernicus_Download-time = ", download_time - start_time, "Hr:min:sec")


def get_extent(shapefile):
    """
    This function takes the original shapefile defining the ROI as input and extracts the extent
    Args:
        shapefile: Path to shapefile (string)
    Returns:
        extent_copernicus: Extent of the shapefile formatted to work with the Copernicus API (string)
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile, 1)
    inLayer = dataSource.GetLayer()
    for feature in inLayer:
        geom = feature.GetGeometryRef()
    raw_extent = geom.GetEnvelope()

    # Each corner of the extent for Copernicus style
    lower_left_c = str(raw_extent[0]) + " " + str(raw_extent[2]) + ","
    upper_left_c = str(raw_extent[0]) + " " + str(raw_extent[3]) + ","
    upper_right_c = str(raw_extent[1]) + " " + str(raw_extent[3]) + ","
    lower_right_c = str(raw_extent[1]) + " " + str(raw_extent[2]) + ","

    # Build string needed for the Copernicus download
    extent_copernicus = "POLYGON ((" + lower_left_c + upper_left_c + upper_right_c + lower_right_c + \
                        lower_left_c[0:len(lower_left_c) - 1] + "))"

    return extent_copernicus
