import os
import rasterio as rio
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
    :return:
        new_list: list
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
    # TODO: add docstrings!
    :param dem_dir:
    :param dem_name:
    :param demType:
    :param shapefile_path:
    :param buffer:
    """
    from spatialist.vector import Vector
    from pyroSAR.gamma.dem import dem_autocreate
    shape_vector = Vector(filename=shapefile_path)
    dem_output = dem_dir + dem_name
    dem_autocreate(geometry=shape_vector, demType=demType, outfile=dem_output, buffer=buffer)


def calculate_multilook_resolution(res):
    """
    Function that calculates number of range and azimuth looks according to desired resolution
    :param res: int
        specifies the output multilook resolution by adjusting range and azimuth multipliers accordingly. Currently only
        20 or multiples thereof allowed (default: 40)
    :return:
        range_looks: string:
            number of range looks to archive desired multilook resolution
        azimuth_looks: string:
            number of azimuth looks to archive desired multilook resolution
    """
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
    # TODO: add docstrings!
    """

    :return:
    """
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
    Function to read textfile with interferogram pairs generated in sbas_graph function
    :return:
        ref_scene_list: list
            returns list of reference scenes according to the SBAS procedure
        coreg_scene_list: list
            returns list of scenes which will be coregistered with their corresponding reference scene
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


def file_for_sbas_graph():
    """
    Function to write SLC_tab list for SBAS inteferogram pairs
    """
    sbas_list = extract_files_to_list(Paths.slc_dir, datatype="vv.slc.iw1.par", datascenes_file=None)
    sbas_list = sorted(sbas_list)
    sbas_nopar_list = []
    for element in sbas_list:
        sbas_nopar_list.append(element[:len(element) - 4])
    merge_list = [sbas_nopar_list, sbas_list]
    with open(Paths.slc_dir + "SLC_tab", "w") as file:
        for x in zip(*merge_list):
            file.write("{0}\t{1}\n".format(*x))


def geocode_back(input_file, range_samples, dem_lut, output_file, out_width):

    # TODO: input_file list or string?
    """
    Function used to geocode image data using a geocoding lookup table
    :param input_file: string
        (input) data file to be geocoded
    :param range_samples: integer
        width of input data file
    :param dem_lut: string
        (input) lookup table containing pairs of real-valued input data coordinates
    :param output_file: string
        (output) output data file
    :param out_width: integer
        width of gc_map lookup table, output file has the same width
    """
    os.system("geocode_back " + input_file + " " + range_samples + " " + dem_lut + " " +
              output_file + " " + out_width + " - 2 0")


def data2geotiff(dem_par_file, geocode_mli, output_file):

    # TODO: input_file list or string?
    """
    Function to convert geocoded data with DEM parameter file to GeoTIFF format
    :param dem_par_file: string
        (input) DIFF/GEO DEM parameter file
    :param geocode_mli: string
        (input) data file
    :param output_file: string
        (output) GeoTIFF file (.tif is the recommended extension)
    """
    os.system("data2geotiff " + dem_par_file + " " + geocode_mli + " 2 " + output_file)


def raster_stack(stackname):
    # TODO: ADD OVERWRITE OPTION!?
    """
    This function stacks the clipped raster files to one raster time series stack for each polarization and flight
    direction
    :param stackname: string
        name of output raster stack of coherence images
    """
    geotiff_list = extract_files_to_list(path_to_folder=Paths.slc_dir, datatype=".tif", datascenes_file=None)
    geotiff_list = sorted(geotiff_list)

    first_band = rio.open(geotiff_list[0], "r")
    meta = first_band.meta.copy()

    # Replace metadata with new count and create a new file
    counts = 0
    for ifile in geotiff_list:
        with rio.open(ifile, 'r') as ff:
            counts += ff.meta['count']
    meta.update(count=counts)

    # Check if filename already exists
    if os.path.exists(Paths.slc_dir + stackname):
        raise Exception("Name for raster stack already exists! Please delete it or specify a new one first!")

    # Write coherence rasterstacks
    with rio.open(Paths.slc_dir + stackname, 'w', **meta) as ff:
        for ii, ifile in enumerate(geotiff_list):
            bands = rio.open(ifile, 'r').read()
            for band in bands:
                ff.write(band, ii + 1)


def import_polygons(shape_path):
    import fiona
    """
    This function imports shapefile from given directory to python
    :param shape_path: string
        Path to shapefile
    :return: list
        Returns a list of all elements in shapefile
    """
    active_shapefile = fiona.open(shape_path, "r")
    for i in range(0, len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
    return shapes


def create_point_buffer(point_path, buffer_size):
    """
    This function is similar to create_shape_buffer but works for point shapefiles
    :param point_path: string
        Path to the shapefile
    :param buffer_size: int
        Buffer size corresponds to the length of the square buffer around the vertex point
    :return: list
        Returns a list with buffered polygons around each point of input polygon
    """
    import_list = import_polygons(shape_path=point_path)
    buffer_size = buffer_size / 2
    buffer_list = []
    for i in range(0, len(import_list)):
        lon = import_list[i]["coordinates"][0]
        lat = import_list[i]["coordinates"][1]

        def create_buffer(lat, lon, buffer_size):
            upper_left = (lon - buffer_size, lat + buffer_size)
            upper_right = (lon + buffer_size, lat + buffer_size)
            lower_left = (lon - buffer_size, lat - buffer_size)
            lower_right = (lon + buffer_size, lat - buffer_size)
            return upper_left, upper_right, lower_left, lower_right

        upper_left, upper_right, lower_left, lower_right = create_buffer(lat, lon, buffer_size)

        buffer_coord = [[upper_left, upper_right, lower_right, lower_left, upper_left]]
        buffer = {"type": "Polygon", "coordinates": buffer_coord}
        buffer_list.append(buffer)
    return buffer_list


def extract_dates(directory):
    """
    Extracts dates from list of preprocessed S-1 GRD files (need to be in standard pyroSAR exported naming scheme!)
    :param directory: string
        Path to folder, where files are stored
    :return: list
        returns list of acquisition dates of S-1 GRD files
    """
    file_list = extract_files_to_list(path_to_folder=directory, datatype=".tif")
    date_list = []
    for file in file_list:
        date_list.append(int(file[2:10]))
    return date_list


def extract_time_series(results_dir, shapefile, buffer_size):
    import numpy as np
    import rasterio.mask
    import rasterio as rio
    import matplotlib.pyplot as plt
    """
    Extracts time series information from patches of pixels using points and a buffer size to specify the size of the
    patch
    :param shapefile: string
        Path to point shapefile including name of shapefile
    :param results_dir: string
        Path to results directory, where layerstacks are stored and csv files will be stored
    :param point_path: string
        Path to point shapefile directory
    :param buffer_size: int
        Buffer size specifies the length of the rectangular buffer around the point
    """
    # Import Patches for each class and all 4 layerstacks (VH/VV/Asc/Desc)
    patches = create_point_buffer(shapefile, buffer_size=buffer_size)
    layer_stacks = extract_files_to_list(path_to_folder=results_dir, datatype=".tif")
    class_list = []
    # Iterate through all layerstacks:
    for file in layer_stacks:
        src1 = rio.open(file)
        patch_mean = []
        # Iterate through all patches of current class
        for patch in patches:
            pixel_mean = []
            out_image, out_transform = rio.mask.mask(src1, [patch], all_touched=1, crop=True, nodata=np.nan)
            # print(len(out_image[0]))
            # Calculate Mean for each patch:
            for pixel in out_image:
                pixel_mean.append(np.nanmean(pixel))
            patch_mean.append(pixel_mean)

        # patch_mean.append(extract_dates(results_dir + "temp" + "/"))

        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = patch_mean.tolist()
        src1.close()
        # print(patch_mean[0])
        class_list.append(patch_mean)

    class_time_series = []
    for example_class in class_list:
        mean_list = []
        for time in example_class:
            mean_list.append(np.mean(time))
        # class_time_series.append(mean_list)
        # print(mean_list)
        # plt.plot(mean_list)
        # plt.show()

    # fig, ax1 = plt.subplots()
    # fig.subplots_adjust(right=0.75)
    # fig.set_figheight(9)
    # fig.set_figwidth(15)
    # print(mean_list)
    # print("iddd")
    return mean_list

    # for elem in mean_list:
    #     # print(elem)
    #     plt.plot(elem)
        # fig, ax1 = plt.subplots()
        # fig.subplots_adjust(right=0.75)
        # fig.set_figheight(9)
        # fig.set_figwidth(15)
        # ax1.plot(elem)
    # plt.show()