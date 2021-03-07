import os


def user_data():
    ###################################     INPUT    ########################################
    home_path = "/home/ki73did/"
    # home_path = "/home/ni82xoj/"

    ############################# Sentinel-1 download parameters ############################
    username = "marlinmm2"
    password = "8DH5BkEre5kykXG"
    api_url = "https://scihub.copernicus.eu/apihub/"
    # Choose the start date of the download interval
    start_date = "2020-06-01"
    # Choose the end date of the download interval
    end_date = "2020-07-30"
    # Choose the satellite, on which the download will be based on (options: "S1A*", "S1B*", "Sentinel-1")
    satellite = "S1A*"
    # Choose the minimum overlap
    min_overlap = 0.1
    # Choose the product you want to download (options: "SLC", "GRD")
    product = "SLC"
    # Do you want to download scenes before processing?
    download = False

    ############################## GAMMA processing parameters ##############################
    # Choose, if single-master or multi-master processing
    processing_step = "single"
    # Choose 0 and processing will be based on only one swath (quicker) or 1: processing with all swaths (slower)
    swath_flag = 0
    # Choose, in which polarization you want to process
    polarization = "vv"
    # Choose your desired multilook resolution (default = 40)
    resolution = 40
    # Choose, which DEM type and buffer distance around the investigation area to use for geocoding
    demType = "SRTM 1Sec HGT"
    buffer = 0.05
    # Choose 1, if temp directories of coregistration should be deleted; if 0: not deleted
    clean_flag = "1"
    # Choose the maximum value of spatial baseline (in meters) for SBAS processing
    bperp_max = 136
    # Choose the maximum value of temporal baseline (in days) for SBAS processing
    delta_T_max = 48
    # Do you want to create a raster stack of geocoded coherence scenes?
    create_rasterstack = False
    # Specify the name of the rasterscene
    # NOTE: if name already exists, rename it, otherwise the creation of the stack will fail
    stackname = "coherence_stack.tif"
    # Do you want to plot the coherence of different land cover classes over time?
    plot_bool = True

    ############################## Auto-creation of needed directories ##############################
    # download_dir = "/geonfs03_vol1/SALDI_EMS/S1_SLC/04_Augrabies/"
    download_dir = home_path + "GEO410_data/"
    # download_dir = home_path + "GAMMA_testdata_1/"

    # text
    shapefile_dir = home_path + "GEO410/Scripts/InSel/shapefiles/augrabies_extent.shp"
    point_samples_dir = home_path + "GEO410/Scripts/InSel/shapefiles/points/"
    orbit_file_dir = home_path + "GEO410_data/orbit_files/"

    return home_path, download_dir, shapefile_dir, point_samples_dir, orbit_file_dir, username, password, api_url, \
           start_date, end_date, satellite, min_overlap, product, download, processing_step, swath_flag, polarization, \
           resolution, demType, buffer, clean_flag, bperp_max, delta_T_max, create_rasterstack, stackname, plot_bool


class Paths(object):
    home_path, download_dir, shapefile_dir, point_samples_dir, orbit_file_dir = user_data()[0:5]

    processing_dir = home_path + "GEO410_data/"
    list_dir = home_path + "GEO410_data/lists/"
    slc_dir = home_path + "GEO410_data/slc/"
    dem_dir = home_path + "GEO410_data/DEM/"

    # TODO: Delete my shit
    # processing_dir = home_path + "GAMMA_testdata_1/"
    # list_dir = home_path + "GAMMA_testdata_1/lists/"
    # slc_dir = home_path + "GAMMA_testdata_1/slc_processing/"
    # dem_dir = home_path + "GAMMA_testdata_1/dem/"

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
    username, password, api_url, start_date, end_date, satellite, min_overlap, product, download = user_data()[5:14]


class Processing(object):
    processing_step, swath_flag, polarization, resolution, demType, buffer, clean_flag, bperp_max, delta_T_max, \
    create_rasterstack, stackname, plot_bool = user_data()[14:]
