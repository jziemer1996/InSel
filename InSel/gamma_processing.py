import os
from support_functions import *
from user_data import Paths


def SLC_import(polarization=None, swath_flag=None):
    """
    Function to read in and concatenate S1 TOPS SLC from zip files
    :param polarization: list
        list containing strings defining the desired polarizations considered during processing e.g. <["vv", "vh"]>
    :param swath_flag: string
        define subswaths to be considered during processing (default = 0 (as listed in
        burst_number_table_ref, all if no burst_number_table_ref provided), 1,2,3 (1 sub-swath only), 4 (1&2), 5 (2&3))
    """
    # set polarization range
    pol_default = ["vv", "vh"]
    pol_list = []
    if polarization is None:
        polarization = pol_default
    for elem in polarization:
        pol_list.append("." + elem.lower())

    # set subswath range
    swath_flag_default = "0"
    if swath_flag is None:
        swath_flag = swath_flag_default

    os.chdir(Paths.slc_dir)

    datascenes_file = Paths.list_dir + "datascenes.zipfile_list"
    deburst_S1_SLC(datascenes_file)

    one_scene_file = Paths.list_dir + "one_scene.zipfile_list"

    with open(datascenes_file, "rt") as slc_zip_list:
        for element in slc_zip_list:
            with open(one_scene_file, 'w') as f:
                f.write(element)
                print(element[:len(element) - 4])
            for pol_type in polarization:
                os.system("S1_import_SLC_from_zipfiles " + one_scene_file + " " + element[:len(element) - 4] +
                          "burst_number_table" + " " + pol_type + " 0 " + swath_flag + " " + Paths.orbit_file_dir + " 1")

        delete_files = ".burst_number_table"
        delete_list = extract_files_to_list(path_to_folder=Paths.slc_dir, datatype=delete_files, datascenes_file=None)
        for file in delete_list:
            os.remove(file)


def multilook(processing_step, res=None):
    """
    Function to calculate MLI mosaic from ScanSAR SLC burst data
    :param processing_step: string
        user specified variable to determine if only main file is multilooked (<"single">) or all
        files (<"multi">) in slc directory are multilooked
    :param res: int
        specifies the output multilook resolution by adjusting range and azimuth multipliers accordingly. Currently only
        20 or multiples thereof allowed (default: 40)
    """
    # define range and azimuth looks based on user-specified input or default values
    range_looks, azimuth_looks = calculate_multilook_resolution(res)

    # set burst window calculation flag to default (0), set to 1 if parameters should be calculated
    default_burst_window_calc_flag = 0

    rlks_azlks_var = " " + range_looks + " " + azimuth_looks

    # get all slc swath files from slc folder
    tab_file_list = extract_files_to_list(Paths.slc_dir, datatype=".SLC_tab", datascenes_file=None)
    tab_file_list = sorted(tab_file_list)

    # execute this branch, if only using coreg and normal preprocessing
    if processing_step == "single":
        output_name = Paths.multilook_dir + tab_file_list[0][len(Paths.slc_dir):len(tab_file_list[0]) - 11]
        os.chdir(Paths.slc_dir)
        os.system("multi_look_ScanSAR " + tab_file_list[0] + " " + output_name + ".mli " + output_name + ".mli.par "
                  + rlks_azlks_var + " " + str(default_burst_window_calc_flag))

    # execute this branch, if using SBAS and special preprocessing
    if processing_step == "multi":
        os.chdir(Paths.slc_dir)
        for slc in tab_file_list:
            output_name = Paths.multilook_dir + slc[len(Paths.slc_dir):len(slc) - 11]
            # os.chdir(Paths.slc_dir)
            os.system("multi_look_ScanSAR " + slc + " " + output_name + ".mli " + output_name + ".mli.par "
                      + rlks_azlks_var + " " + str(default_burst_window_calc_flag))


def gc_map(processing_step, demType, buffer):
    """
    Function that creates a DEM in Gamma format for a defined spatial geometry and calculates terrain-geocoding lookup
    table and DEM derived data products
    :param processing_step: string
        user specified variable to determine if only main file is processed or all files will be processed
    :param demType: string
        the type of DEM to be used; current options:
            - "AW3D30"
            - "SRTM 1Sec HGT"
            - "SRTM 3Sec"
            - "TDX90m"
    :param buffer: float
        a buffer in degrees to create around the geometry
    """
    # GAMMA default values for additional output parameter represented by "-"
    # oversampling factors (float)
    lat_ovr = "- "
    lon_ovr = "- "
    r_ovr = "- "

    # output files (can be specified as strings)
    sim_sar = "- "
    zen_angle = "- "
    ori_angle = "- "
    loc_inc_angle = "- "
    proj_angle = "- "
    pix_norm_factor = "- "

    # number of additional DEM pixel to add around area covered by SAR image
    frame = "- "
    # LUT values for regions with layover,shadows or DEM gaps (can range from 0 to 3 -> default 2)
    ls_mode = "- "

    # get all mli.par files from multilook folder
    mli_file_list = extract_files_to_list(Paths.multilook_dir, datatype=".mli.par", datascenes_file=None)
    mli_file_list = sorted(mli_file_list)

    # execute this branch, if only using coreg and normal preprocessing
    if processing_step == "single":
        main_mli = mli_file_list[0]

        # Automatically create DEM and DEM_par files using pyroSAR:
        dem_name = main_mli[len(main_mli) - 16:len(main_mli) - 8] + ".dem"
        create_dem_for_gamma(Paths.dem_dir, dem_name, demType, Paths.shapefile_dir, buffer)

        dem_par = Paths.dem_dir + dem_name + ".par "
        dem = Paths.dem_dir + dem_name + " "
        dem_seg_par = Paths.dem_dir + dem_name + "_seg.par "
        dem_seg = Paths.dem_dir + dem_name + "_seg "
        dem_lut = Paths.dem_dir + dem_name + "_lookup.lut "

        os.system("gc_map " + main_mli + " - " + dem_par + dem + dem_seg_par + dem_seg + dem_lut + lat_ovr + lon_ovr
                  + sim_sar + zen_angle + ori_angle + loc_inc_angle + proj_angle + pix_norm_factor + frame + ls_mode
                  + r_ovr)

    # execute this branch, if using SBAS and special preprocessing
    if processing_step == "multi":
        for mli in mli_file_list:
            # Automatically create DEM and DEM_par files using pyroSAR:
            dem_name = mli[len(mli) - 16:len(mli) - 8] + ".dem"
            create_dem_for_gamma(Paths.dem_dir, dem_name, demType, Paths.shapefile_dir, buffer)

            dem_par = Paths.dem_dir + dem_name + ".par "
            dem = Paths.dem_dir + dem_name + " "
            dem_seg_par = Paths.dem_dir + dem_name + "_seg.par "
            dem_seg = Paths.dem_dir + dem_name + "_seg "
            dem_lut = Paths.dem_dir + dem_name + "_lookup.lut "

            os.system("gc_map " + mli + " - " + dem_par + dem + dem_seg_par + dem_seg + dem_lut + lat_ovr + lon_ovr
                      + sim_sar + zen_angle + ori_angle + loc_inc_angle + proj_angle + pix_norm_factor + frame + ls_mode
                      + r_ovr)


def geocode_dem(processing_step):
    """
    Function for forward geocoding transformation using a lookup table
    :param processing_step: string
        user specified variable to determine if only main file is processed or all files will be processed
    """
    # get all .lut files from dem folder
    lut_list = extract_files_to_list(Paths.dem_dir, datatype=".lut", datascenes_file=None)
    lut_list = sorted(lut_list)
    # get all mli.par files from multilook folder
    mli_par_list = extract_files_to_list(Paths.multilook_dir, datatype=".mli.par", datascenes_file=None)
    mli_par_list = sorted(mli_par_list)
    # get all .dem_seg.par files from dem folder and create a new list
    dem_seg_list = []
    dem_seg_list_in = extract_files_to_list(Paths.dem_dir, datatype=".dem_seg.par", datascenes_file=None)
    # need to extract .dem.par files for further processing, but functions finds .dem_seg_par too
    # thats why: append name of elements without datatype in dem_seg_list_in to new list
    for elem in dem_seg_list_in:
        dem_seg_list.append(elem[:len(elem) - 4])
    dem_seg_list = sorted(dem_seg_list)
    # get all .dem.par files from dem folder
    dem_par_list = extract_files_to_list(Paths.dem_dir, datatype=".dem.par", datascenes_file=None)
    dem_par_list = sorted(dem_par_list)
    # define names of .dem.par files as output name for hgt
    hgt_out_list = []
    for file in dem_par_list:
        hgt_out_list.append(file[:len(file) - 8] + "_out.rdc_hgt")

    # execute this branch, if only using coreg and normal preprocessing
    if processing_step == "single":
        mli_par_dict = get_par_as_dict(mli_par_list[0])
        range_samples = mli_par_dict.get("range_samples")
        azimuth_lines = mli_par_dict.get("azimuth_lines")

        dem_par_dict = get_par_as_dict(dem_par_list[0])
        dem_width = dem_par_dict.get("width")

        os.system("geocode " + lut_list[0] + " " + dem_seg_list[0] + " " + dem_width + " " + hgt_out_list[0] + " "
                  + range_samples + " " + azimuth_lines + " - -")

    # execute this branch, if using SBAS and special preprocessing
    if processing_step == "multi":
        for i, mli_par in enumerate(mli_par_list):
            mli_par_dict = get_par_as_dict(mli_par)
            range_samples = mli_par_dict.get("range_samples")
            azimuth_lines = mli_par_dict.get("azimuth_lines")
            print(azimuth_lines)

            dem_par_dict = get_par_as_dict(dem_par_list[i])
            dem_width = dem_par_dict.get("width")
            os.system("geocode " + lut_list[i] + " " + dem_seg_list[i] + " " + dem_width + " " + hgt_out_list[i] + " "
                      + range_samples + " " + azimuth_lines + " - -")


def coreg(processing_step, polarization, clean_flag, res=None):
    """
    Function to coregister a Sentinel-1 TOPS mode burst SLC to a reference burst SLC
    :param processing_step: string
        user specified variable to determine if scenes of a raster stack are only coregistered on the first reference
        burst SLC or (single master approach) or if all files are coregistered dynamically according to their
        spatio-temporal baselines (multi master approach with SBAS technique (Small Baseline Subsets)
    :param polarization: string
        string defining the desired polarization considered during processing (choose "vv" or "vh")
        :param clean_flag: string
        flag to indicate if intermediate files are deleted
            - 0: not deleted
            - 1: deleted (default)
    :param res: int
        specifies the output multilook resolution by adjusting range and azimuth multipliers accordingly. Currently only
        20 or multiples thereof allowed (default: 40)
        NOTE: resolution must be the same value as in the multilook function; in default mode already accomplished by
        "None"!!!
    """
    import shutil

    # define range and azimuth looks based on user-specified input or default values
    range_looks, azimuth_looks = calculate_multilook_resolution(res)

    pol = polarization
    # get all .SLC_tab files from dem folder
    tab_file_list = extract_files_to_list(Paths.slc_dir, datatype=".SLC_tab", datascenes_file=None)
    tab_file_list = sorted(tab_file_list)
    tab_pol_list = []
    # check, if data scenes fullfill specified polarization type and if yes, append files to new list
    for element in tab_file_list:
        if pol in element:
            tab_pol_list.append(element)

    # generate .RSLC_tab files as input variable for coregistration
    rslc_list = []
    for tab in tab_pol_list:
        if pol in tab:
            rslc_file = tab[:len(tab) - 8] + ".RSLC_tab"
            shutil.copy2(tab, rslc_file)
            # Read in the file
            with open(rslc_file, 'r') as file:
                filedata = file.read()

            # Replace the target string
            filedata = filedata.replace('slc', 'rslc')

            # Write the file out again
            with open(rslc_file, 'w') as file:
                file.write(filedata)

            rslc_list.append(rslc_file)

    pol_list = []
    for file in tab_pol_list:
        if pol in file:
            file_name = file[len(Paths.slc_dir):len(file) - 11]
            pol_list.append(file_name)

    os.chdir(Paths.slc_dir)
    # get all .rdc_hgt files from dem folder
    rdc_hgt_list = extract_files_to_list(Paths.dem_dir, datatype=".rdc_hgt", datascenes_file=None)
    rdc_hgt_list = sorted(rdc_hgt_list)

    # execute this branch, if only using coreg and normal preprocessing
    if processing_step == "single":
        for i in range(0, len(tab_pol_list) - 1):
            os.system("S1_coreg_TOPS " + tab_pol_list[0] + " " + pol_list[0] + " " + tab_pol_list[i + 1] + " "
                      + pol_list[i + 1] + " " + rslc_list[i + 1] + " " + rdc_hgt_list[0] + " "
                      + range_looks + " " + azimuth_looks + " - - - - - " + clean_flag)

    # execute this branch, if using SBAS and special preprocessing
    if processing_step == "multi":
        # SBAS function needs to be run here to get SLC_tab file with interferometry pairs for coregistration
        file_for_sbas_graph()
        rslc_par_list = sbas_graph()

        if not os.path.exists(rslc_par_list[0]):
            os.system("S1_coreg_TOPS " + tab_pol_list[0] + " " + pol_list[0] + " " + tab_pol_list[1] + " "
                      + pol_list[1] + " " + rslc_list[1] + " " + rdc_hgt_list[0] + " "
                      + range_looks + " " + azimuth_looks + " - - - - - " + clean_flag)

        # extract reference list and coreg list from sbas output
        ref_scene_list, coreg_scene_list = read_file_for_coreg()

        for i, ref in enumerate(ref_scene_list):
            SLC1_tab = ref + "." + polarization + ".SLC_tab"
            SLC2_tab = coreg_scene_list[i] + "." + polarization + ".SLC_tab"
            RSLC_tab = coreg_scene_list[i] + "." + polarization + ".RSLC_tab"

            hgt_list = Paths.dem_dir + ref + "_out.rdc_hgt"

            os.system("S1_coreg_TOPS " + Paths.slc_dir + SLC1_tab + " " + ref + " " + Paths.slc_dir + SLC2_tab + " " +
                      coreg_scene_list[i] + " " + Paths.slc_dir + RSLC_tab + " " + hgt_list + " " + range_looks
                      + " " + azimuth_looks + " - - - - - " + clean_flag)


def coherence_calc():
    """
    Function to estimate interferometric correlation coefficient
    """
    # need to extract .diff files for further processing, but function finds .diff.bmp
    # thats why: append name of elements without datatype in diff_bmp_list to new list
    diff_bmp_list = extract_files_to_list(Paths.slc_dir, datatype=".diff.bmp", datascenes_file=None)
    diff_bmp_list = sorted(diff_bmp_list)
    diff_list = []
    for element in diff_bmp_list:
        diff_list.append(element[:len(element) - 4])

    mli_par_list = extract_files_to_list(Paths.multilook_dir, datatype=".mli.par", datascenes_file=None)
    mli_par_list = sorted(mli_par_list)
    if len(mli_par_list) == 1:
        mli_par_dict = get_par_as_dict(mli_par_list[0])
        range_samples = mli_par_dict.get("range_samples")
    if len(mli_par_list) > 1:
        diff_for_mli_list = []
        for element in diff_list:
            diff_for_mli_list.append(Paths.multilook_dir + element[len(element) - 22:len(element) - 14] + ".mli.par")
        for mli_par in diff_for_mli_list:
            mli_par_dict = get_par_as_dict(mli_par)
            range_samples = mli_par_dict.get("range_samples")

    for diff in diff_list:
        os.system("cc_wave " + diff + " - - " + diff[:len(diff)-5] + ".cc " + range_samples)


def sbas_graph():
    """

    :return:
    """
    rslc_path_list = extract_files_to_list(Paths.slc_dir, datatype=".rslc.par", datascenes_file=None)
    rslc_path_list = sorted(rslc_path_list)
    rslc_par_list = []
    for elem in rslc_path_list:
        rslc_par_list.append(elem[len(Paths.slc_dir):len(elem)])
    print(rslc_par_list)
    os.system("base_calc " + Paths.slc_dir + "/SLC_tab " + Paths.slc_dir + rslc_par_list[0] + " " + Paths.slc_dir +
              "baseline_plot.out " + Paths.slc_dir + "baselines.txt " + "1 1 - 136 - 48")

    return rslc_par_list


def geocode_coherence():
    """

    :param slc_dir:
    :param dem_dir:
    :return:
    """
    cc_list = extract_files_to_list(Paths.slc_dir, datatype=".cc", datascenes_file=None)
    cc_list = sorted(cc_list)

    # TODO: support_functions if possible!
    diff_list = []
    for element in cc_list:
        diff_list.append(element[:len(element) - 4])
    mli_par_list = extract_files_to_list(Paths.multilook_dir, datatype=".mli.par", datascenes_file=None)
    mli_par_list = sorted(mli_par_list)
    print(mli_par_list)
    if len(mli_par_list) == 1:
        mli_par_dict = get_par_as_dict(mli_par_list[0])
        range_samples = mli_par_dict.get("range_samples")
    if len(mli_par_list) > 1:
        for mli_par in mli_par_list:
            mli_par_dict = get_par_as_dict(mli_par)
            range_samples = mli_par_dict.get("range_samples")

    lut_list = []
    dem_par_list = []
    for element in cc_list:
        lut_list.append(Paths.dem_dir + element[len(element) - 20:len(element) - 12] + ".dem_lookup.lut")
        dem_par_list.append(Paths.dem_dir + element[len(element) - 20:len(element) - 12] + ".dem.par")

        if len(dem_par_list) == 1:
            dem_width_dict = get_par_as_dict(dem_par_list[0])
            out_width = dem_width_dict.get("width")
        if len(dem_par_list) > 1:
            for dem_par in dem_par_list:
                dem_width_dict = get_par_as_dict(dem_par)
                out_width = dem_width_dict.get("width")

    for i, cc in enumerate(cc_list):
        geocode_file = cc[:len(cc)-3] + ".mli"
        output_file = cc[:len(cc)-3] + ".tif"
        geocode_back(input_file=cc, range_samples=range_samples, dem_lut=lut_list[i],
                     output_file=geocode_file, out_width=out_width)

        data2geotiff(dem_par_file=dem_par_list[i], geocode_mli=geocode_file, output_file=output_file)
