import os
import logging
import json

from datetime import datetime
from collections import OrderedDict
from osgeo import gdal
from osgeo import gdalconst

import click
import numpy as np
import shutil

import inspect
import traceback
import sys


VERSION = 'v1.0.0'


@click.command()
@click.argument('filename')
def cli(filename, type=click.Path(exists = True)):
    try:
        dataset = gdal.Open(filename, 0) # read-only => external overviews
        pyramids = create_pyramids(dataset)
        click.echo('Created pyramids of levels ' + str(pyramids))
    except Exception as e:
        logging.error(str(e) +"\n" + traceback.extract_tb(sys.exc_info()[2]).format()[-1])    

def create_pyramids(dataset, levels = 5, jpeg_quality = 75):
    ''' Generates pyramids for FILENAME '''
    try:

        pstart = datetime.utcnow()

        gdal.UseExceptions()

        bit_depth = gdal.GetDataTypeName(dataset.GetRasterBand(1).DataType)
        if bit_depth == 'Float32':
            compress_overview = 'LZW'
        else:
            compress_overview = 'JPEG'
            gdal.SetConfigOption('JPEG_QUALITY_OVERVIEW', str(jpeg_quality))

        pyramids = [ 2**j for j in range(1,levels+1) ]

        gdal.SetConfigOption('COMPRESS_OVERVIEW', compress_overview)
    except Exception as ex:
        logging.error("Could not determine compression type from raw data. Check raster band.")
        raise ex
    try:
        dataset.BuildOverviews("BILINEAR", [2,4,8,16,32])
    except Exception as e:
        logging.error("Failed to save overviews in tiff directory. Check permissions.")
        raise e

    print(str((datetime.utcnow()-pstart).total_seconds()), "seconds elapsed for pyramids")

    return pyramids