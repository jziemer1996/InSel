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
    :return: new_list: list
        returns list of paths to files
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(datatype):
            new_list.append(os.path.join(path_to_folder, filename[:(len(filename))]))
        else:
            continue
    with open(datascenes_file, 'w') as f:
        for item in new_list:
            f.write("%s\n" % item)
    return new_list


def deburst_S1_SLC(path_to_folder, datatype):
    datascenes_file = path_to_folder + 'datascenes.asc'
    print(datascenes_file)
    zip_file_list = extract_files_to_list(path_to_folder, datatype, datascenes_file)
    for i in range(len(zip_file_list)):
        master_file = zip_file_list[i]
        print("Masterfile is...:" + master_file)
        os.system("S1_BURST_tab_from_zipfile " + "-" + " " + master_file)


def SLC_import(path_to_folder, datatype):

