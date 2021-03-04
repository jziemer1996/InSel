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


    ##### GAMMA functions for processing: #####

    def processing(processing_step, swath_flag, polarization, resolution, demType, buffer, clean_flag, bperp_max,
                   delta_T_max, create_rasterstack, stackname):

        # SLC_import(polarization=[Processing.polarization], swath_flag=swath_flag)
        #
        # multilook(processing_step, resolution)
        #
        # gc_map(processing_step, demType, buffer)
        #
        # geocode_dem(processing_step)

        # coreg(processing_step, clean_flag, bperp_max, delta_T_max, polarization, resolution)

        # coherence_calc()

        geocode_coherence(create_rasterstack, stackname)


    ######### Decide, which way to execute ############

    ##### Data download function: #####
    if DownloadParams.download:
        sentinel_download.copernicus_download()

    processing(processing_step=Processing.processing_step, swath_flag=Processing.swath_flag,
               polarization=Processing.polarization, resolution=Processing.resolution, demType=Processing.demType,
               buffer=Processing.buffer, clean_flag=Processing.clean_flag, bperp_max=Processing.bperp_max,
               delta_T_max=Processing.delta_T_max, create_rasterstack=Processing.create_rasterstack,
               stackname=Processing.stackname)

    end_time = datetime.now()
    print("######### Successfully finished processing! #########")
    print("#####################################################")
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
    print("#####################################################")
