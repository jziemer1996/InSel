"""
Main function to initialize variables, directories and user data and for calling/executing the desired functions
Authors: Marlin Mueller <marlin.markus.mueller@uni-jena.de>, Jonas Ziemer <jonas.ziemer@uni-jena.de>
"""

###########################################################
# imports
###########################################################

import os
import json
from datetime import datetime
import sentinel_api
from InSel.sentinel_download import *


def main():

    download_dir = "F:/GEO410/download"
    shapefile_dir = "F:/GEO410/shapefile"
    print("Hello!")

    copernicus_download(copernicus_username, copernicus_password, download_directory, api_url, satellite, min_overlap,
                        timeliness, start_date, end_date, product, orig_shape)


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("Processing-time = ", end_time - start_time, "Hr:min:sec")