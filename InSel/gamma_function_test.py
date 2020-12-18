import os


def display_slc():
    os.system("disSLC /home/ni82xoj/GEO410/DISP/orig/05721.slc 2500")


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


def deburst_S1_SLC(processing_dir, download_dir, list_dir):
    if not os.path.exists(list_dir):
        os.makedirs(list_dir)
    datascenes_file = list_dir + 'datascenes.zipfile_list'
    print(datascenes_file)
    zip_file_list = extract_files_to_list(download_dir, datatype=".zip", datascenes_file=datascenes_file)
    for file in zip_file_list:
        file_name = file[file.find("S1A"):len(file)-4] + ".burst_number_table"
        print(file_name)
        print("Masterfile is...:" + file)
        os.system("S1_BURST_tab_from_zipfile" + " - " + file)
        os.replace(file_name, processing_dir + file_name)


def SLC_import(slc_dir, list_dir):
    datascenes_file = list_dir + 'datascenes.zipfile_list'
    one_scene_file = list_dir + "one_scene.zipfile_list"
    if not os.path.exists(slc_dir):
        os.makedirs(slc_dir)
    with open(datascenes_file, "rt") as slc_zip_list:
        for element in slc_zip_list:
            with open(one_scene_file, 'w') as f:
                    f.write(element)
            os.system("S1_import_SLC_from_zipfiles " + one_scene_file + " " + element[:len(element)-4] +
                      "burst_number_table" + " - 0 0 . 1")
        pol_list = [".vh", ".vv"]
        for pol in pol_list:
            import_file_list = extract_files_to_list(os.getcwd(), datatype=pol, datascenes_file=None)
            print(import_file_list)
            for file in import_file_list:
                index = file.find(pol)
                filename = file[index-8:]
                os.replace(file, slc_dir + filename)


def define_precise_orbits(slc_dir, orbit_dir):
    nstate = 60
    par_file_list = extract_files_to_list(slc_dir, datatype=".par", datascenes_file=None)
    par_file_list = sorted(par_file_list)

    for parfile in par_file_list:
        os.system(os.getcwd() + "/OPOD_vec_lola.pl " + parfile + " " + orbit_dir + " " + nstate)
