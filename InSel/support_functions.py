import os
from user_data import *


def create_dem_for_gamma(dem_dir, shapefile_path):
    """

    :param dem_dir:
    :param shapefile_path:
    :return:
    """
    from spatialist.vector import Vector
    from pyroSAR.gamma.dem import dem_autocreate
    shape_vector = Vector(filename=shapefile_path)
    dem_autocreate(geometry=shape_vector, demType="SRTM 1Sec HGT", outfile=dem_dir + "dem_final.dem", buffer=0.05)


def geocode_back():
    """

    :param slc_dir:
    :param dem_dir:
    :return:
    """
    os.system("geocode_back " + Paths.slc_dir + "20201025.vv.mli " + "9685 " + Paths.dem_dir + "DEM_final_lookup.lut "
              + Paths.slc_dir + "20201025.vv_geocode.mli " + "3290 " + "- 2 0")


def data2geotiff():
    """

    :param dem_dir:
    :param slc_dir:
    :return:
    """
    os.system("data2geotiff " + Paths.dem_dir + "dem_final.dem.par " + Paths.slc_dir + "20201025.vv_geocode.mli " + "2 "
              + Paths.slc_dir + "output3.tif")


def display_slc():
    os.system("disSLC /home/ni82xoj/GEO410/DISP/orig/05721.slc 2500")


def get_par_as_dict(path):
    # path = "C:/Users/marli/Downloads/20201001.vv.slc.iw1.par"
    par_file = open(path, 'r')
    par_dict = {}

    # iterate through lines of par file
    for line in par_file:
        # remove newline statements at end of each line with "-1"
        cleaned_line = line[0:len(line)-1]
        # check for lines containing ":" as separator
        if ":" in cleaned_line:
            # create key by extracting name
            index = cleaned_line.index(":")
            key = cleaned_line[0:index]

            # create value by extracting everything right of ":"
            temp_value = cleaned_line[index + 1:]
            value = temp_value.strip()

            # append to dict
            par_dict.update({key: value})
    return par_dict
