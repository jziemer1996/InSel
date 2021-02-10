import sentinel_api as s3api
from datetime import datetime
from osgeo import ogr
from user_data import DownloadParams, Paths


def copernicus_download(satellite, min_overlap, product):
    """
    This function takes the user input to create a API call for the Copernicus Hub and downloads the specified data.
    Args:
        copernicus_username: Username for the Copernicus Hub (string)
        copernicus_password: Password for the Copernicus Hub (string)
        download_directory: Directory where downloaded files are stored (string)
        api_url: URL for the API (string)
        satellite: Satellite, from which data should be downloaded (write as: "S3A*" oder "S3B*" or "Sentinel-3" for the
            different Sentinel-3 satellite platforms or both) (string)
        min_overlap: Define minimum overlap (0-1) between area of interest and scene footprint (Default: 0) (float)
        timeliness: Define recent and historical scenes (write: "Near Real Time" or "Short Time Critical" or "Non Time
            Critical") (string)
        start_date: Define starting date of search (Default: None, all data) (string)
        end_date: Define ending date of search (Default: None, all data) (string)
        product: Select wanted Sentinel product (write as: "*LST*" or "*WST*") (string)
        orig_shape: Path to shapefile specified in settings.txt for download and subsequent clipping (string)
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
    s1.search(satellite, min_overlap, Paths.download_dir, DownloadParams.start_date, DownloadParams.end_date,
              producttype=product)

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
        extent_dias: Extent of the shapefile formatted to work with the DIAS API (string)
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
