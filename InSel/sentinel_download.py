import sentinel_api as s3api
from datetime import datetime


def copernicus_download(copernicus_username, copernicus_password, download_directory, api_url, satellite, min_overlap,
                        timeliness, start_date, end_date, product, orig_shape):
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
    s3 = s3api.SentinelDownloader(copernicus_username, copernicus_password, api_url)

    # Set download directory
    s3.set_download_dir(download_directory)

    # Set bounding box for area of investigation
    # polygon = misc_functions.get_extent(shapefile=orig_shape)[0]
    # s3.set_geometries(polygon)

    # Search for corresponding data scenes via api
    s3.search(satellite, min_overlap, download_directory, start_date, end_date, producttype=product,
              timeliness=timeliness)

    # Download data - returns dictionary of downloaded data scenes
    # (Format: {'failed': ['', '', ..], 'success': ['', '', '', ..]})
    s3.download_all()

    download_time = datetime.now()
    print("Copernicus_Download-time = ", download_time - start_time, "Hr:min:sec")