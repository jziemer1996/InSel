import os


def user_data():
    # home_path = "/home/ki73did/"
    home_path = "/home/ni82xoj/"

    # download_dir = "/geonfs03_vol1/SALDI_EMS/S1_SLC/04_Augrabies/"
    # download_dir = home_path + "GEO410_data/"
    download_dir = home_path + "GAMMA_testdata_1/"

    # text
    shapefile_dir = home_path + "GEO410/Scripts/InSel/shapefiles/augrabies_extent.shp"
    # TODO: ORBIT FILES DIRECTORY??????
    orbit_file_dir = home_path + "GEO410_data/orbit_files/"

    # Sentinel-1 download parameters
    username = "marlinmm2"
    password = "8DH5BkEre5kykXG"
    api_url = "https://scihub.copernicus.eu/apihub/"
    start_date = "2020-06-01"
    end_date = "2020-07-30"
    satellite = "S1A*"
    min_overlap = 0.1
    product = "SLC"

    # GAMMA processing parameters
    processing_step = "multi"
    swath_flag = 0
    polarization = "vv"
    resolution = 40
    demType = "SRTM 1Sec HGT"
    buffer = 0.05
    clean_flag = "1"
    bperp_max = 136
    delta_T_max = 48
    stackname = "res_stack_in_dir.tif"

    return home_path, download_dir, shapefile_dir, orbit_file_dir, username, password, api_url, start_date, end_date, \
           satellite, min_overlap, product, processing_step, swath_flag, polarization, resolution, demType, buffer, \
           clean_flag, bperp_max, delta_T_max, stackname


class Paths(object):
    home_path, download_dir, shapefile_dir, orbit_file_dir = user_data()[0:4]

    # processing_dir = home_path + "GEO410_data/"
    # list_dir = home_path + "GEO410_data/lists/"
    # slc_dir = home_path + "GEO410_data/slc/"
    # dem_dir = home_path + "GEO410_data/DEM/"

    processing_dir = home_path + "GAMMA_testdata_1/"
    list_dir = home_path + "GAMMA_testdata_1/lists/"
    slc_dir = home_path + "GAMMA_testdata_1/slc/"
    dem_dir = home_path + "GAMMA_testdata_1/DEM/"

    multilook_dir = slc_dir + "multilook/"
    results_dir = slc_dir + "coherence_results/"
    stack_dir = results_dir + "rasterstack/"

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
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    if not os.path.exists(stack_dir):
        os.makedirs(stack_dir)


class DownloadParams(object):
    username, password, api_url, start_date, end_date, satellite, min_overlap, product = user_data()[4:12]


class Processing(object):
    processing_step, swath_flag, polarization, resolution, demType, buffer, clean_flag, bperp_max, delta_T_max, \
    stackname = user_data()[12:]
