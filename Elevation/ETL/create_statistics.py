import click
import logging

import sys
import traceback

from osgeo import gdal
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from datetime import datetime

@click.command()
@click.argument('filename', type=click.Path(exists=True))                 # must be a .tif file
@click.option('--give_output', is_flag=True)
def cli(filename, give_output = False):          #C:\Users\sparimi\Desktop\GeoTIF_Files\cdem_dem_010O_tif\cdem_dem_010O.tif

    try:
        dataset = gdal.Open(filename, 0) # 0 = read-only
        create_statistics(filename, dataset, give_output)
    except Exception as ex:
        print("create_statistics failed to run for file {0}".format(filename))
        logging.error("create_statistics failed to run for file {0}".format(filename))
        raise ex


def create_statistics(filename, dataset, give_output = False):
    ''' Calculates statistics for FILENAME '''
    start = datetime.utcnow()
    gdal.UseExceptions()

    # ========= LOAD DATA AND CALCULATE STATISTICS =========
    try:

        num_bands = dataset.RasterCount
        for x in range(num_bands):
            band = dataset.GetRasterBand(x+1)
            stats = band.GetStatistics(0,1)         # 0 = approx is NOT ok      1 = force
            generate_xml(stats, filename, str(x+1), give_output)

    except RuntimeError as ex:
        logging.warning("Failed to generate statistics: no valid pixels found in samplng for {0}".format(filename))

    
    except Exception as ex:
            logging.error("Could not calculate statistics for {0}".format(filename))
            raise ex

    print(str((datetime.utcnow()-start).total_seconds()), "seconds elapsed for statistics of file {0}".format(filename))


def generate_xml(stats, filename, passed_band, give_output = False):
    """ Creates xml file to record the statistics.  """

    try:
        # ========= SETUP BASIC FILE STRUCTURE =========
        PAMDataset = ET.Element('PAMDataset')
        PAMRasterBand = ET.SubElement(PAMDataset, 'PAMRasterBand', band=passed_band)
        Metadata = ET.SubElement(PAMRasterBand, 'Metadata')
        max = ET.SubElement(Metadata, 'MDI', key="STATISTICS_MAXIMUM")
        min = ET.SubElement(Metadata, 'MDI', key="STATISTICS_MINIMUM")
        mean = ET.SubElement(Metadata, 'MDI', key="STATISTICS_MEAN")
        stddev = ET.SubElement(Metadata, 'MDI', key="STATISTICS_STDDEV")
        
    except Exception as ex:
        logging.warning("generate_XML failed to setup XML file structure for file {0}".format(filename))
        raise ex

    try:  
        # ========= SETS VALUES =========
        max.text = str(stats[0])
        min.text = str(stats[1])
        mean.text = str(stats[2])
        stddev.text = str(stats[3])

    except Exception as ex:
        logging.warning("generate_XML failed to add statistics to file {0}".format(filename))
        raise ex

    try:
        # ========= FORMATS DATA =========
        rough_data = ET.tostring(PAMDataset, encoding='unicode')        #converts data from bytes to strings
        formatted_data = (parseString(rough_data)).toprettyxml(indent='    ')                 #formats data

    except Exception as ex:
        logging.warning("generate_XML failed to format XML data for file {0}".format(filename))
        raise ex

    if give_output:
        print(formatted_data)

    # ========= WRITE TO FILE =========
    try:
        myfile = open(filename+".aux.xml", 'w')
        myfile.write(formatted_data)

    except Exception as ex:
        logging.warning("Failed to write data to file {0}.aux.xml).".format(filename))
        raise ex