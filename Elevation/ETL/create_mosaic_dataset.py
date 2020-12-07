import arcpy
import argparse
import ConfigParser
import os
import logging
from datetime import datetime

 # C:/Python27/ArcGIS10.3/python.exe c:/Users/sparimi/EdrGIT/RaD/EdrCore/USGS/Elevation/ETL/create_mosaic_dataset.py

'''
try:
        # =========  READS PATH TO RASTER FILES FROM CONFIG FILE =========
        config = ConfigParser.ConfigParser()
        config.read('Elevation/ETL/config.ini')
        DEM = config.get('MAIN','DEM')
        DEST_DIR = config.get('MAIN','DEST_DIR')
        indir = os.path.join(DEST_DIR, DEM)                            # "\\GisFile01\USGS_Elevation\CDEM_30"          C:/Users/sparimi/Desktop/Script_Mosaic1"
        outdir = os.path.join(DEST_DIR, DEM)                              # "C:/Users/sparimi/Desktop/sravan_test"

except Exception as ex:
        logging.error("Could not read input directory from config file")
        print(ex)


try:
        # ========= TAKES OPTIONAL ARGUMENTS FROM COMMANDLINE =========
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--outdir", default = "indir", help= "give the path to folder where geodatabase will be stored")
        parser.add_argument("-i", "--indir", default = "outdir", help = "give path to folder with raster data to be put in the Mosaic Dataset")
        # parser.add_argument("data_model", default = DEM, help = "give elevation data model: CDEM or USGS")           
        args = parser.parse_args()
        outdir = args.outdir
        indir = args.indir
        # model = args.model

except Exception as ex:
        logging.error("Encountered problem with parsing arguments indir and outdir. See =help")
        raise ex
'''

indir = "C:/Temp/CDEM_30" # "C:/Users/sparimi/Desktop/data"          #
outdir = indir

print(indir)

def create_mosaic_dataset(outdir, indir):
        ''' creates a Mosaic Dataset and loads raster data into the Mosaic '''        
        
        # ========= SETS UP OUTPUT DIRECTORY AS AN ARPY ENVIRONMENT =========
        try:
                arcpy.env.workspace = outdir

        except Exception as ex:
                logging.error("Failed to set up ArcPy environment workspace {0}".format(workspace))
                raise ex

        start = datetime.utcnow()
        
        # ========= CREATES FILE GEODATABASE =========
        gdbName = "Geodatabase.gdb"
        
        try:        
                if os.path.exists(os.path.join(outdir, gdbName)):
                        logging.warning("Deleting pre-existing geodatabase...")
                        os.remove(outdir+"/"+gdbName)
        
        except:
                logging.error("Failed to delete preexisting file {0}. Creating new file newGeodatabase.gdb".format(gdbName))
                gdbName = "newGeodatabase.gdb"

        try:
                arcpy.CreateFileGDB_management(outdir, gdbName)

        except Exception as ex:
                logging.error("Failed to create geodatabase {0}".format(gdbName))
                raise ex

        # ========= CREATES MOSAIC DATASET ========= 
        try:
                mdName = "script_mosaic"
                prjfile = "3857"
                numbands = "1"
                pixel_type = "8_BIT_SIGNED"
                arcpy.CreateMosaicDataset_management(gdbName, mdName, prjfile, numbands, pixel_type)

        except Exception as ex:
                logging.error("Failed to create mosaic dataset {0}".format(mdName))
                raise ex
        
        # ========= LOADS RASTER DATA INTO MOSAIC =========
        try:
                rasterType = "Raster Dataset"
                arcpy.AddRastersToMosaicDataset_management((gdbName+"/"+mdName), rasterType, indir)

        except:
                logging.error("Failed to load rasters from {0} to mosaic dataset".format(indir))
                raise ex

        print(str((datetime.utcnow()-start).total_seconds()), "seconds elapsed.")

create_mosaic_dataset(outdir, indir)