import os


def user_data():
    # home_path = "/home/ki73did/"
    home_path = "/home/ni82xoj/"

    # download_dir = "/geonfs03_vol1/SALDI_EMS/S1_SLC/04_Augrabies/"
    # download_dir = home_path + "GEO410_data/"
    download_dir = home_path + "GAMMA_testdata/"

    # text
    shapefile_dir = home_path + "GEO410/Scripts/InSel/shapefiles/augrabies_extent.shp"
    orbit_file_dir = home_path + "GEO410_data/orbit_files/"

    username = "marlinmm2"
    password = "8DH5BkEre5kykXG"
    api_url = "https://scihub.copernicus.eu/apihub/"
    start_date = "2020-06-01"
    end_date = "2020-07-30"

    return home_path, download_dir, shapefile_dir, orbit_file_dir, username, password, api_url, start_date, end_date


class Paths(object):
    home_path, download_dir, shapefile_dir, orbit_file_dir = user_data()[0:4]

    # processing_dir = home_path + "GEO410_data/"
    # list_dir = home_path + "GEO410_data/lists/"
    # slc_dir = home_path + "GEO410_data/slc/"
    # dem_dir = home_path + "GEO410_data/DEM/"

    processing_dir = home_path + "GAMMA_testdata/"
    list_dir = home_path + "GAMMA_testdata/lists/"
    slc_dir = home_path + "GAMMA_testdata/slc/"
    dem_dir = home_path + "GAMMA_testdata/DEM/"

    multilook_dir = slc_dir + "multilook/"

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(shapefile_dir):
        raise Exception("No shapefile found, please specify shapefile location including shapefile name")
    if not os.path.exists(orbit_file_dir):
        raise Exception("No orbit file directory found, please specify location and add files to location")
    if not os.path.exists(processing_dir):
        os.makedirs(processing_dir)
    if not os.path.exists(list_dir):
        os.makedirs(list_dir)
    if not os.path.exists(slc_dir):
        os.makedirs(slc_dir)
    if not os.path.exists(dem_dir):
        os.makedirs(dem_dir)
    if not os.path.exists(multilook_dir):
        os.makedirs(multilook_dir)


class DownloadParams(object):
    username, password, api_url, start_date, end_date = user_data()[4:9]
