import click
import os
import logging

from datetime import datetime
import csv

import gdal
import osr

import inspect
import traceback
import sys

import json

VERSION = 'v1.0.0'

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--human-readable', is_flag=True)
def cli(filename, human_readable=False):
    try:
        dataset = gdal.Open(filename, 0)
        data = create_metadata(filename, dataset, human_readable)
        print(json.dumps(data, indent=4))
    except Exception as ex:
        logging.error(str(ex) +"\n" + traceback.extract_tb(sys.exc_info()[2]).format()[0])   

def create_metadata(filename, dataset, human_readable = False):
    """  Retrieve gdalinfo-esque metadata of geotiff passed as arg.  """

    start = datetime.utcnow()


    # ========== FILE INFO ==========
    try:
        path = filename
        extension = os.path.splitext(filename)[1]
        created = os.path.getctime(filename)
        modified = os.path.getmtime(filename)
        size = os.path.getsize(filename)
    except Exception as ex:
        logging.error("Incorrect File Name.")
        raise ex

    try:
        if human_readable:
            created = datetime.fromtimestamp(created).isoformat()
            modified = datetime.fromtimestamp(modified).isoformat()
            size = str(size/1048576) + "MB"
    except Exception as ex:
        logging.error("File is not created correctly.")
        raise ex

    gdal.UseExceptions()

    # ========== IMAGE INFO ==========
    try:
        width = dataset.RasterXSize
        height = dataset.RasterYSize
        bit_depth = gdal.GetDataTypeName(dataset.GetRasterBand(1).DataType)
        compression = dataset.GetMetadata('IMAGE_STRUCTURE').get('COMPRESSION', 'None') # None if uncompressed
        bands = dataset.RasterCount
    except Exception as ex:
        logging.warning("Information is not calculated correctly.")
        raise ex

    # ========== SPATIAL INFO ==========
    try:
        prj = dataset.GetProjection()
        srs=osr.SpatialReference(wkt=prj)

        epsg = srs.GetAttrValue('AUTHORITY',1)
        gcs = srs.GetAttrValue('geogcs')
        unit = srs.GetAttrValue('unit')

        ulx, xres, xskew, uly, yskew, yres  = dataset.GetGeoTransform()
        lrx = ulx + (dataset.RasterXSize * xres)
        lry = uly + (dataset.RasterYSize * yres)

        cell_size = (xres, yres)
        extent = [(ulx, uly), (lrx, lry)]
    except Exception as ex:
        logging.warning("Incorrect dataset.")
        raise ex

    # ========== WRITE CSV ==========
    file_csv = os.path.splitext(filename)[0] + '.csv'

    try:
        with open(file_csv, mode='w') as csv_file:
            fieldnames = ['path', 'extension', 'created', 'modified', 'size', 'associated_files', 
                            'width', 'height', 'bit_depth', 'compression', 'bands',
                            'gcs', 'epsg', 'cell_size', 'unit', 'extent'] #gcs = geospatial coordinate system
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            row = {
                'path'          : path,
                'extension'     : extension, 
                'created'       : created,
                'modified'      : modified,
                'size'          : size,
                'width'         : width,
                'height'        : height,
                'bit_depth'     : bit_depth,
                'compression'   : compression,
                'bands'         : bands,
                'gcs'           : gcs,
                'epsg'          : epsg,
                'cell_size'     : cell_size,
                'unit'          : unit,
                'extent'        : extent}

            writer.writeheader()
            writer.writerow(row)

            print(str((datetime.utcnow() - start).total_seconds()) + " seconds elapsed for create_metadata of file {}".format(filename))

            return row
    except Exception as e:
        raise e

    
