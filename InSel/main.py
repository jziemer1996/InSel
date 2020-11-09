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


def main():
    print("Hello!")


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("Processing-time = ", end_time - start_time, "Hr:min:sec")