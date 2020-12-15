"""
Main function to initialize variables, directories and user data and for calling/executing the desired functions
Authors: Marlin Mueller <marlin.markus.mueller@uni-jena.de>, Jonas Ziemer <jonas.ziemer@uni-jena.de>
"""

###########################################################
# imports
###########################################################
import os
import sentinel_download
import gamma_function_test


def main():
    # home_path = "/home/ki73did"
    home_path = "/home/ni82xoj/"

    download_dir = home_path + "GEO410_data/"
    shapefile_dir = home_path + "/GEO410/Scripts/InSel/shapefiles/thuringia.shp"

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    username = "marlinmm2"
    password = "8DH5BkEre5kykXG"
    api_url = "https://scihub.copernicus.eu/apihub/"
    start_date = "2020-06-01"
    end_date = "2020-06-16"

    # s1 = SentinelDownloader(username, password, api_url='https://scihub.copernicus.eu/apihub/')
    # s1.set_geometries(
    #     'POLYGON ((13.501756184061247 58.390759025092443,13.617310497771715 58.371827474899703,13.620921570075168 58.27891592167088,13.508978328668151 58.233319081414017,13.382590798047325 58.263723491583974,13.382590798047325 58.263723491583974,13.501756184061247 58.390759025092443))')
    # s1.set_download_dir('./')  # default is current directory
    # s1.search('S1A*', 0.8, productType='GRD', sensoroperationalmode='IW')
    # s1.write_results(type='wget', file='test.sh.neu')  # use wget, urls or json as type
    # s1.download_all()
    #
    #
    # s1 = SentinelDownloader(username, password, api_url='https://scihub.copernicus.eu/apihub/')
    # # s1.load_sites('wetlands_v8.shp')
    # s1.set_geometries(
    #     'POLYGON ((13.501756184061247 58.390759025092443,13.617310497771715 58.371827474899703,13.620921570075168 58.27891592167088,13.508978328668151 58.233319081414017,13.382590798047325 58.263723491583974,13.382590798047325 58.263723491583974,13.501756184061247 58.390759025092443))')
    # s1.set_download_dir('./')  # default is current directory
    #
    # # set additional directories which contain downloaded scenes.
    # # A scene is only going to be downloaded if it does not yet exist in either of the data directories or the download directory.
    # s1.set_data_dir('/path/to/datadir1')
    # s1.set_data_dir('/path/to/datadir2')
    #
    # s1.search('S1A*', 0.8, productType='GRD', sensoroperationalmode='IW')
    # s1.write_results(file_type='wget', filename='sentinel_api_download.sh')  # use wget, urls or json as type
    # s1.download_all()

    # sentinel_download.copernicus_download(copernicus_username=username, copernicus_password=password, download_directory=download_dir,
    #                     api_url=api_url, satellite="S1A*", min_overlap=0.1, start_date=start_date, end_date=end_date,
    #                     product="SLC", orig_shape=shapefile_dir)

    # gamma_function_test.display_slc()

    # gamma_function_test.extract_files_to_list(path_to_folder=home_path, datatype=".zip")
    gamma_function_test.deburst_S1_SLC(path_to_folder=home_path, datatype=".zip")


if __name__ == '__main__':
    main()

