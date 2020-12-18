import os


def display_slc():
    os.system("disSLC /home/ni82xoj/GEO410/DISP/orig/05721.slc 2500")


def extract_files_to_list(path_to_folder, datatype, datascenes_file):
    """
    function to extract files of given datatype from given directory and return as a list
    :param datascenes_file:
    :param path_to_folder: string
        path to folder, where files are to be extracted from
    :param datatype: string
        datatype of files to return from given folder
    :return: new_list: list
        returns list of paths to files
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(datatype):
            new_list.append(os.path.join(path_to_folder, filename))
        else:
            continue
    with open(datascenes_file, 'w') as f:
        for item in new_list:
            f.write("%s\n" % item)
    return new_list


def deburst_S1_SLC(path_to_folder):
    datascenes_file = path_to_folder + 'datascenes.zipfile_list'
    print(datascenes_file)
    zip_file_list = extract_files_to_list(path_to_folder, datatype=".zip", datascenes_file=datascenes_file)

    for file in zip_file_list:
        file_name = file[file.find("S1"):len(file)-4] + ".burst_number_table"
        print("Masterfile is...:" + file)
        os.system("S1_BURST_tab_from_zipfile" + " - " + file)

        os.replace(file_name, path_to_folder + file_name)


def SLC_import(path_to_folder):
    datascenes_file = path_to_folder + 'datascenes.zipfile_list'
    one_scene_file = path_to_folder + "one_scene.zipfile_list"
    with open(datascenes_file, "rt") as slc_zip_list:
        for element in slc_zip_list:
            with open(one_scene_file, 'w') as f:
                    f.write(element)
            os.system("S1_import_SLC_from_zipfiles " + one_scene_file + " " + element[:len(element)-4] + "burst_number_table"
                      + " - 0 0 . 1")
