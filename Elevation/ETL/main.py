import configparser
import os
from datetime import datetime

import click
import ftputil
import gdal

from usgs_url_list import usgs_url_list
from cdem_url_list import cdem_url_list
from create_metadata import create_metadata
from create_pyramids import create_pyramids
from create_statistics import create_statistics
from dem_to_edr import dem_to_tmp, get_tmp_dem_dir, tmp_to_edr

config = configparser.ConfigParser()
config.read('Elevation\\ETL\\config.ini')
DEM = config['MAIN']['DEM']


elevation_files = [] # elevation images

if DEM == "CDEM_30":

    squares = ['012', '022', '023'] #squares to be downloaded


    previous = squares #pattern matched downloads to be skipped

    urls = cdem_url_list(sqrs=squares)

    for prev in previous:
        urls = list(filter(lambda x: prev not in x, urls))

    dem_to_tmp(urls)
    start = datetime.utcnow()
    download_time = (datetime.utcnow()-start).total_seconds()
    tmp_dem_dir = get_tmp_dem_dir()

    for root, directories, filenames in os.walk(tmp_dem_dir):
        for filename in filenames: 
            f = os.path.join(root,filename)
            if f.endswith(".tif"):
                elevation_files.append(f)

if DEM == "3DEP_10":
    urls = usgs_url_list('ned_connecticut.csv')

    #dem_to_tmp(urls)
    start = datetime.utcnow()
    download_time = (datetime.utcnow()-start).total_seconds()
    tmp_dem_dir = get_tmp_dem_dir()

    ## HAVE TO FIGURE OUT HOW TO FIND FILE (are they all w001001.adf?)
    for root, directories, filenames in os.walk(tmp_dem_dir):
        for filename in filenames: 
            f = os.path.join(root,filename)
            if f.endswith('001.adf'):
                elevation_files.append(f)



for f in elevation_files:
    print("running scripts for {}".format(f))
    dstart = datetime.utcnow()
    dataset = gdal.Open(f)
    print(str((datetime.utcnow()-dstart).total_seconds()), "seconds elapsed for dataset {}".format (f))
    
    create_metadata(f, dataset)
    
    create_pyramids(dataset)
    
    create_statistics(f, dataset)


# COPY FILES TO EDR

tmp_to_edr()

print(str(download_time), "seconds elapsed for download")

print(str((datetime.utcnow()-start).total_seconds()), "seconds elapsed for main")
