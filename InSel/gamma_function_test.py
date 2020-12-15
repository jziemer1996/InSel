import os


def display_slc():
    os.system("disSLC /home/ni82xoj/GEO410/DISP/orig/05721.slc 2500")

def deburst_S1_SLC():
    os.system("S1_BURST_tab_from_zipfile /home/ni82xoj/GEO410_data/")
