import csv
import click
import logging
import traceback
import sys


@click.command()
@click.argument('csv_path', type=click.Path(exists=True)) #".\\ned_continental.csv"
def cli(csv_path):
    try:
        usgs_url_list(csv_path)
    except Exception as ex:
        logging.error(str(ex) +"\n" + traceback.extract_tb(sys.exc_info()[2]).format()[-1])    





def usgs_url_list(csv_path):
    
    urls = []

    with open(csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter =',')
        line_count =0
        for row in csv_reader:
            url = row['downloadURL']
            urls.append(url)
            line_count += 1

    print(urls)
    print(len(urls))
    return urls