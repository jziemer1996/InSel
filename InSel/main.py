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
    sentinel_download.copernicus_download()

    ##### GAMMA functions for processing: #####

    def coreg_only(processing_step, swath_flag, polarization, resolution, demType, buffer, clean_flag, bperp_max,
                   delta_T_max, stackname):

        SLC_import(polarization=[Processing.polarization], swath_flag=swath_flag)

        multilook(processing_step, resolution)

        gc_map(processing_step, demType, buffer)

        geocode_dem(processing_step)

        coreg(processing_step, clean_flag, bperp_max, delta_T_max, polarization, resolution)


    def SBAS_processing(processing_step, swath_flag, polarization, resolution, demType, buffer, clean_flag, bperp_max,
                        delta_T_max, stackname):

        SLC_import(polarization=[Processing.polarization], swath_flag=swath_flag)

        multilook(processing_step, resolution)

        gc_map(processing_step, demType, buffer)

        geocode_dem(processing_step)

        coreg(processing_step, clean_flag, bperp_max, delta_T_max, polarization, resolution)

        # coherence_calc()
        # geocode_coherence()

        # raster_stack(stackname="SLC_coherence.tif")

    coreg_only()
    # SBAS_processing()

    end_time = datetime.now()
    print("#####################################################")
    print("processing-time = ", end_time - start_time, "Hr:min:sec")
    print("#####################################################")


