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
from datetime import datetime


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

        SLC_import(polarization=["vv"], swath_flag=0)

        # define_precise_orbits() # probably not needed anymore

        multilook(processing_step, res=40)

        gc_map()

        # geocode_dem()

        # coreg()


    def SBAS_processing(processing_step="multi"):

        SLC_import(polarization=["vv"])

        # define_precise_orbits() # probably not needed anymore

        multilook(processing_step)

        gc_map()

        # geocode_dem()

        # coreg()



    end_time = datetime.now()
    print("#####################################################")
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
    print("#####################################################")

