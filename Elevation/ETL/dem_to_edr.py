import configparser
import inspect
import logging
import os
import re
import shutil
import sys
import tempfile
import traceback
import urllib.request
import zipfile
from datetime import datetime

import click
from pySmartDL import SmartDL


'''
downloads and unpacks a zip "zip_name.zip" 
located at url "https://dem.website/folder01/zip_name.zip" 
to the following directory structure in dem_dir/

dem_dir/
	├╴download/
    │   └╴folder01/
	│	    └╴zip_name.zip
    └╴data/
        └╴folder01/
            ├╴zip_contents_file_1
            ├╴zip_contents_file_2
            │ ...
            └╴zip_contents_file_n

Note that for USGS, folder01 read from the url is ambiguous, and so the coordinate location (eg n50w123) is used instead

To test from virtual environment run the following command:

zip_to_edr "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/ArcGrid/USGS_NED_13_n50w123_ArcGrid.zip"

'''


@click.command()
@click.argument('url')
@click.option('-m', '--move-to-dest', 'move', is_flag=True)
def cli(url, move):
    try:
        zip_to_tmp(url)
        if (move):
            tmp_to_edr()
    except Exception as ex:
        logging.error("\n")
        logging.error(str(ex) +"\n" + traceback.extract_tb(sys.exc_info()[2]).format()[-1])   


def _copyfileobj_patched(fsrc, fdst, length=16*1024*1024):
    """Patches shutil method to hugely improve copy speed"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
shutil.copyfileobj = _copyfileobj_patched


def _copytree_patched(src, dst):
    """Patches shutil method to allow overwrites"""
    my_files = [] # list of lists of format [abs_file, rel_file]

    for dir, subdir, files in os.walk(src):
        for file in files:
            abs_file = os.path.join(dir, file)
            print("abs_file is {}".format(abs_file))

            rel_dir = os.path.relpath(dir,src) #gets rid of .\ at start of relative path
            rel_file = os.path.join(rel_dir, file)

            print("rel_file is {}".format(rel_file))


            list_ = [abs_file, rel_file]

            my_files.append(list_)

    for list_ in my_files:
        rel_path = list_[1]
        if ".\\" in rel_path:
            list_[1] = rel_path[2:]

    for f in my_files:
        #print(f[0])
        dest_path = os.path.join(dst, f[1])
        #print("copying {} to {} . . .".format(f[0], dest_path))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(f[0], dest_path)
shutil.copytree = _copytree_patched

def get_tmp_dem_dir():
    config = configparser.ConfigParser()
    config.read('Elevation\\ETL\\config.ini')
    TEMP_DIR = config['MAIN']['TEMP_DIR']
    DEM = config['MAIN']['DEM']
    tmp_dem_dir = os.path.join(TEMP_DIR, DEM)
    return tmp_dem_dir


def zip_to_tmp(url):
    '''
    Downloads zip_name.zip from url string to file hosted online
    Saves zip_name.zip to tempdir and unpacks it there
    Copies over zip to parent_dir\download\zip_name.zip
    Copies over extracted contents into the directory parent_dir\zip_name\\
    '''
    try:

        down_start = datetime.utcnow()

        config = configparser.ConfigParser()
        config.read('Elevation\\ETL\\config.ini')
        DEM = config['MAIN']['DEM']

        zip_name_and_ext = os.path.basename(url) # eg zip_name.zip
        if DEM =='CDEM_30' :
            subdir_name = os.path.basename(os.path.dirname(url)) #eg 001 (CDEM) or n29w098 (3DEP)
        elif DEM == "3DEP_10" :
            print(zip_name_and_ext)
            regex = re.compile('n..w...')
            start = re.search(regex, zip_name_and_ext).start()
            subdir_name = zip_name_and_ext[start:start+7]

        
        tmp_dem_dir = get_tmp_dem_dir()

        tmp_down_dir = os.path.join(tmp_dem_dir, "download")
        tmp_down_sub_dir = os.path.join(tmp_down_dir, subdir_name)
        tmp_zip_path = os.path.join(tmp_down_sub_dir, zip_name_and_ext)

        
        tmp_extr_dir = os.path.join(tmp_dem_dir, "data")
        tmp_extr_sub_dir = os.path.join(tmp_extr_dir, subdir_name)


        if not os.path.exists(tmp_down_sub_dir):
            os.makedirs(tmp_down_sub_dir)
        if not os.path.exists(tmp_extr_sub_dir):
            os.makedirs(tmp_extr_sub_dir)


        if os.path.exists(tmp_zip_path):
            os.remove(tmp_zip_path)
        print("downloading {}".format(zip_name_and_ext))
        #downloader = Downloader(url, tmp_zip_path, 8)
        #downloader.start()
        #downloader.wait_for_finish()
        #wget.download(url, tmp_zip_path)
        #urllib.request.urlretrieve(url, tmp_zip_path)  

        #headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

        #r = requests.get(url, headers=headers_)

        #with open(tmp_zip_path, 'wb') as f:
        #    f.write(r.content)

        obj = SmartDL(url, tmp_zip_path)
        obj.start()

        print("extracing {}".format(zip_name_and_ext))
        zip_ref = zipfile.ZipFile(tmp_zip_path, 'r')
        zip_ref.extractall(tmp_extr_sub_dir)
        zip_ref.close()

        print(str((datetime.utcnow()-down_start).total_seconds()), "seconds elapsed for dataset {}".format (url))

    except Exception as ex:
        raise
    
def dem_to_tmp(urls, sleep=30):
    '''
    Downloads and unpacks a list containing strings of urls to zips hosted online
    '''
    for url in urls:
        time.sleep(sleep)
        zip_to_tmp(url)
	
def tmp_to_edr():
    '''
    copies the whole of dem_dir to destination.
    '''
    tmp_dem_dir = get_tmp_dem_dir()

    config = configparser.ConfigParser()
    config.read('Elevation\\ETL\\config.ini')
    DEST_DIR = config['MAIN']['DEST_DIR']
    DEM = config['MAIN']['DEM']

    dest_dem_dir = os.path.join(DEST_DIR, DEM)
    print(dest_dem_dir)


    shutil.copytree(tmp_dem_dir, dest_dem_dir)
