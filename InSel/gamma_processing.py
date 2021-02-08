import os
import shutil
from gamma_support_functions import *
from user_data import *


def extract_files_to_list(path_to_folder, datatype, datascenes_file):
    """
    function to extract files of given datatype from given directory and return as a list
    :param path_to_folder: string
        path to folder, where files are to be extracted from
    :param datatype: string
        datatype of files to return from given folder
    :param datascenes_file:
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

    """
    # datascenes_file = Paths.list_dir + 'datascenes.zipfile_list'
    print(datascenes_file)
    zip_file_list = extract_files_to_list(Paths.download_dir, datatype=".zip", datascenes_file=datascenes_file)
    for file in zip_file_list:
        file_name = file[file.find("S1A"):len(file) - 4] + ".burst_number_table"
        print(file_name)
        print("Masterfile is...:" + file)
        os.system("S1_BURST_tab_from_zipfile" + " - " + file)
        os.replace(file_name, Paths.processing_dir + file_name)


def SLC_import():
    """

    """
    datascenes_file = Paths.list_dir + "datascenes.zipfile_list"
    deburst_S1_SLC(datascenes_file)

    one_scene_file = Paths.list_dir + "one_scene.zipfile_list"

    with open(datascenes_file, "rt") as slc_zip_list:
        for element in slc_zip_list:
            with open(one_scene_file, 'w') as f:
                f.write(element)
                print(element[:len(element) - 4])
            os.system("S1_import_SLC_from_zipfiles " + one_scene_file + " " + element[:len(element) - 4] +
                      "burst_number_table" + " - 0 0 " + Paths.orbit_file_dir + " 1")
        pol_list = [".vv"]
        delete_list = [".vv", ".vh"]
        for pol in pol_list:
            import_file_list = extract_files_to_list(os.getcwd(), datatype=pol, datascenes_file=None)
            print(import_file_list)
            for file in import_file_list:
                index = file.find(pol)
                filename = file[index - 8:]
                print(file)
                shutil.move(file, Paths.slc_dir + filename)

            for datascene in delete_list:
                import_delete_list = extract_files_to_list(os.getcwd(), datatype=datascene, datascenes_file=None)
                print(import_delete_list)
                for ele in import_delete_list:
                    os.remove(ele)


# def define_precise_orbits():
#     """
#
#     """
#     nstate = 60
#     par_file_list = extract_files_to_list(Paths.slc_dir, datatype=".par", datascenes_file=None)
#     par_file_list = sorted(par_file_list)
#
#     for parfile in par_file_list:
#         os.system(os.getcwd() + "/OPOD_vec_lola.pl " + parfile + " " + Paths.orbit_file_dir + " " + str(nstate))


def multilook():
    """

    :param slc_dir:
    :return:
    """

    tab_file_list = extract_files_to_list(Paths.slc_dir, datatype=".SLC_tab", datascenes_file=None)
    tab = sorted(tab_file_list)
    print(tab[0])
    os.chdir(Paths.slc_dir)
    # TODO: nochmal die multi-look factors ueberpruefen
    os.system("multi_look_ScanSAR " + tab[0] + " " + tab[0][:len(tab[0]) - 11] + ".mli " +
              tab[0][:len(tab[0]) - 11] + ".mli.par" + " 8 2 0")


def gc_map():
    """

    """
    # Automatically create DEM and DEM_par files using pyroSAR:
    create_dem_for_gamma(Paths.dem_dir, Paths.shapefile_dir)

    # Extract first .mli based on date to select as master scene:
    mli_file_list = extract_files_to_list(Paths.slc_dir, datatype=".mli.par", datascenes_file=None)
    mli_file_list = sorted(mli_file_list)
    print(mli_file_list)
    master_mli = mli_file_list[0]
    print(master_mli)
    os.system("gc_map " + master_mli + " - " + Paths.dem_dir + "dem_final.dem.par " + Paths.dem_dir + "dem_final.dem "
              + Paths.dem_dir + "DEM_final_seg.par " + Paths.dem_dir + "DEM_final_seg " + Paths.dem_dir
              + "DEM_final_lookup.lut " + "- - - - - - - - - - - -")


def geocode_dem():
    """

    """
    os.system("geocode " + Paths.dem_dir + "DEM_final_lookup.lut " + Paths.dem_dir + "DEM_final_seg " + "3290 " +
              Paths.dem_dir + "DEM_final_out.rdc_hgt " + "8474 6790 " + "- -")


def coreg():
    """

    :param slc_dir:
    :param dem_dir:
    :return:
    """
    import shutil
    pol = "vv"
    tab_file_list = extract_files_to_list(Paths.slc_dir, datatype=".SLC_tab", datascenes_file=None)
    tab_file_list = sorted(tab_file_list)
    tab_pol_list = []
    for element in tab_file_list:
        if pol in element:
            tab_pol_list.append(element)
    print(tab_file_list)

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
    print(rslc_list)

    pol_list = []
    for file in tab_pol_list:
        if pol in file:
            file_name = file[len(Paths.slc_dir):len(file) - 11]
            pol_list.append(file_name)

    print("tab_pol_list=")
    print(tab_pol_list)
    print("pol_list=")
    print(pol_list)
    print("rslc_list=")
    print(rslc_list)

    os.chdir(Paths.slc_dir)
    for i in range(0, len(tab_pol_list) - 1):
        os.system("S1_coreg_TOPS " + tab_pol_list[0] + " " + pol_list[0] + " " + tab_pol_list[i + 1] + " "
                  + pol_list[i + 1] + " " + rslc_list[i + 1] + " " + Paths.dem_dir + "DEM_final_out.rdc_hgt"
                  + " 8 2 - - - - - 0")
