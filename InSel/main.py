"""
Main function to initialize variables, directories and user data and for calling/executing the desired functions
Authors: Marlin Mueller <marlin.markus.mueller@uni-jena.de>, Jonas Ziemer <jonas.ziemer@uni-jena.de>
"""

###########################################################
# imports
###########################################################
import os
import sentinel_download
from gamma_processing import *
from support_functions import *
from datetime import datetime
import matplotlib.pyplot as plt


if __name__ == '__main__':
    start_time = datetime.now()

    ##### Data download function: #####
    # sentinel_download.copernicus_download(copernicus_username=DownloadParams.username,
    #                                       copernicus_password=DownloadParams.password,
    #                                       download_directory=Paths.download_dir,
    #                                       api_url=DownloadParams.api_url, satellite="S1A*",
    #                                       min_overlap=0.1, start_date=DownloadParams.start_date,
    #                                       end_date=DownloadParams.end_date, product="SLC",
    #                                       orig_shape=Paths.shapefile_dir)

    ##### GAMMA functions for processing: #####

    def coreg_only(processing_step="single"):

        SLC_import(polarization=["vv"])

        # define_precise_orbits() # probably not needed anymore

        multilook(processing_step="single")

        # gc_map(processing_step="single", demType="SRTM 1Sec HGT", buffer=0.05)

        # geocode_dem()

        coreg()


    def SBAS_processing(processing_step="multi"):

        SLC_import(polarization=["vv"])

        # define_precise_orbits() # probably not needed anymore

        multilook(processing_step="multi")
        #
        # gc_map(processing_step="multi", demType="SRTM 1Sec HGT", buffer=0.05)
        #
        # geocode_dem(processing_step)

        # coreg(processing_step, polarization="vv", res=None, clean_flag="0")

        # sbas_graph()

    # coreg_only()
    # SBAS_processing()
    point_path = "C:/Users/marli/Google Drive/Studium/Master/2.Semester/GEO410/Daten/Shapefiles/"
    results_dir = "C:/Users/marli/Google Drive/Studium/Master/2.Semester/GEO410/Daten/Koheränzen/"
    point_list = extract_files_to_list(path_to_folder=point_path, datatype=".shp")
    print(point_list)
    test_list = []
    for shapefile in point_list:
        test_list.append(extract_time_series(results_dir=results_dir, shapefile=shapefile, buffer_size=0.001))
    print(test_list)
    for elem in test_list:
        plt.plot(elem)
    plt.show()


    end_time = datetime.now()
    print("#####################################################")
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
    print("#####################################################")


