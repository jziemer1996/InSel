import os
from user_data import *


def extract_files_to_list(path_to_folder, datatype, datascenes_file=None):
    """
    Function to extract files of given datatype from given directory and return as a list
    :param path_to_folder: string
        path to folder, where files are to be extracted from
    :param datatype: string
        datatype of files to return from given folder
    :param datascenes_file: string
        if filename is specified, list is exported to file
    :return: new_list: list
        returns list of paths to files
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if datatype in filename:
            new_list.append(os.path.join(path_to_folder, filename))
        else:
            continue
    if datascenes_file is not None:
        with open(datascenes_file, 'w') as f:
            for item in new_list:
                f.write("%s\n" % item)
    return new_list


def deburst_S1_SLC(datascenes_file):
    """
    Function used to generate S1_BURST_tab to support burst selection
    :param datascenes_file: string
        if filename is specified, list is exported to file
    """
    zip_file_list = extract_files_to_list(Paths.download_dir, datatype=".zip", datascenes_file=datascenes_file)
    for file in zip_file_list:
        file_name = file[file.find("S1A"):len(file) - 4] + ".burst_number_table"
        print("Mainfile is...:" + file)
        os.system("S1_BURST_tab_from_zipfile" + " - " + file)
        os.replace(file_name, Paths.processing_dir + file_name)


def create_dem_for_gamma(dem_dir, dem_name, demType, shapefile_path, buffer):
    """

    :param buffer:
    :param demType:
    :param dem_name:
    :param dem_dir:
    :param shapefile_path:
    :return:
    """
    from spatialist.vector import Vector
    from pyroSAR.gamma.dem import dem_autocreate
    shape_vector = Vector(filename=shapefile_path)
    dem_output = dem_dir + dem_name
    # dem_autocreate(geometry=shape_vector, demType="SRTM 1Sec HGT", outfile=dem_output, buffer=0.05)
    dem_autocreate(geometry=shape_vector, demType=demType, outfile=dem_output, buffer=buffer)


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


def calculate_multilook_resolution(res):
    # allow user-defined resolutions in increments of 20m
    default_resolution = 40

    if res is None:
        res = default_resolution
        range_looks = 8
        azimuth_looks = 2
    if res is not None and res % 20 == 0:
        range_looks = int(res / 5)
        azimuth_looks = int(res / 20)
    if res is not None and res % 20 != 0:
        raise Exception("resolution should be multiple of 20m, default is set to 40m")
    return str(range_looks), str(azimuth_looks)


def get_par_as_dict(path):
    # path = "C:/Users/marli/Downloads/20201001.vv.slc.iw1.par"
    par_file = open(path, 'r')
    par_dict = {}

    # iterate through lines of par file
    for line in par_file:
        # remove newline statements at end of each line with "-1"
        cleaned_line = line[0:len(line) - 1]
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


def read_file_for_coreg():
    """

    :return:
    """
    file = Paths.slc_dir + "baseline_plot.out"
    columns = []
    ref_scene_list = []
    coreg_scene_list = []
    with open(file, 'r') as token:
        for line in token:
            test = line.splitlines()[0]
            columns.append(test.split())
        for elem in columns:
            ref_scene_list.append(elem[1])
            coreg_scene_list.append(elem[2])

    return ref_scene_list, coreg_scene_list


def geocode_back(input_file, range_samples, dem_lut, output_file, out_width):
    """

    :param slc_dir:
    :param dem_dir:
    :return:
    """
    os.system("geocode_back " + input_file + " " + range_samples + " " + dem_lut + " " +
              output_file + " " + out_width + " - 2 0")



def data2geotiff(dem_par_file, geocode_mli, output_file):
    """

    :param dem_dir:
    :param slc_dir:
    :return:
    """
    os.system("data2geotiff " + dem_par_file + " " + geocode_mli + " 2 " + output_file)