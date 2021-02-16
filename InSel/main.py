"""
Main function to initialize variables, directories and user data and for calling/executing the desired functions
Authors: Marlin Mueller <marlin.markus.mueller@uni-jena.de>, Jonas Ziemer <jonas.ziemer@uni-jena.de>
"""

###########################################################
# imports
###########################################################
import os
import sentinel_download
import gamma_processing
from datetime import datetime


def main():
    start_time = datetime.now()
    # home_path = "/home/ki73did/"
    home_path = "/home/ni82xoj/"

    # download_dir = "/geonfs03_vol1/SALDI_EMS/S1_SLC/04_Augrabies/"
    download_dir = home_path + "GEO410_data/"

    dem_dir = download_dir + "DEM/"

    shapefile_dir = home_path + "GEO410/Scripts/InSel/shapefiles/augrabies_extent.shp"

    processing_dir = home_path + "GEO410_data/"
    list_dir = home_path + "GEO410_data/lists/"
    slc_dir = home_path + "GEO410_data/slc/"
    orbit_dir = home_path + "GEO410_data/orbit_files/"

######################################
    # download_dir = home_path + "GAMMA_testdata/"
    # dem_dir = download_dir + "DEM/"
    # shapefile_dir = home_path + "GEO410/Scripts/InSel/shapefiles/augrabies_extent.shp"
    # processing_dir = home_path + "GAMMA_testdata/"
    # list_dir = home_path + "GAMMA_testdata/lists/"
    # slc_dir = home_path + "GAMMA_testdata/slc/"
######################################

    # Settings for data download:
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    username = "marlinmm2"
    password = "8DH5BkEre5kykXG"
    api_url = "https://scihub.copernicus.eu/apihub/"
    start_date = "2020-06-01"
    end_date = "2020-07-30"

    # Data download function:
    # sentinel_download.copernicus_download(copernicus_username=username, copernicus_password=password,
    #                                       download_directory=download_dir, api_url=api_url, satellite="S1A*",
    #                                       min_overlap=0.1, start_date=start_date, end_date=end_date,
    #                                       product="SLC", orig_shape=shapefile_dir)

    # GAMMA functions for processing:
    # gamma_function_test.display_slc()

    # gamma_processing.deburst_S1_SLC(processing_dir=processing_dir, download_dir=download_dir, list_dir=list_dir)
    #
    # gamma_processing.SLC_import(slc_dir=slc_dir, list_dir=list_dir)
    #
    # gamma_processing.define_precise_orbits(slc_dir=slc_dir, orbit_dir=orbit_dir)
    #
    # gamma_processing.multilook(slc_dir=slc_dir)
    # # TODO: hier funktioniert der Übergang zwischen den Funktionen nicht fehlerfrei <-- Bei mir schon... ;)
    #
    # gamma_processing.gc_map(slc_dir=slc_dir, dem_dir=dem_dir, shapefile_path=shapefile_dir)
    #
    # gamma_processing.geocode_dem(dem_dir=dem_dir)

    # gamma_processing.coreg(slc_dir=slc_dir, dem_dir=dem_dir)

    # gamma_processing.file_for_sbas_graph(slc_dir)

    # gamma_processing.sbas_graph(slc_dir)

    # gamma_processing.spectral_diversity_points(slc_dir)

    gamma_processing.readfileforcoreg(slc_dir)

    # gamma_function_test.geocode_back(slc_dir=slc_dir, dem_dir=dem_dir)
    #
    # gamma_function_test.data2geotiff(dem_dir=dem_dir, slc_dir=slc_dir)

    end_time = datetime.now()
    print("#####################################################")
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
    print("#####################################################")


if __name__ == '__main__':
    main()

