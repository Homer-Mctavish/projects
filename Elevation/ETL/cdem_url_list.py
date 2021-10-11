import ftputil
import os
import click


FTP_HOST = "ftp.geogratis.gc.ca"
FTP_DIR  = "/pub/nrcan_rncan/elevation/cdem_mnec/"

all_sqrs = ['001', '002', '003', '010', '011', '012', '013', '014', '015', '016', 
    '020', '021', '022', '023', '024', '025', '026', '027', '029', 
    '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', 
    '040', '041', '042', '043', '044', '045', '046', '047', '048', '049', 
    '051', '052', '053', '054', '055', '056', '057', '058', '059', 
    '062', '063', '064', '065', '066', '067', '068', '069', 
    '072', '073', '074', '075', '076', '077', '078', '079', 
    '082', '083', '084', '085', '086', '087', '088', '089', 
    '092', '093', '094', '095', '096', '097', '098', '099', 
    '102', '103', '104', '105', '106', '107', 
    '114', '115', '116', '117', 
    '120', 
    '340', 
    '560']


@click.command()
def cli():
    try:
        cdem_url_list()
    except Exception as ex:
        print(ex)

def cdem_url_list(sqrs = all_sqrs):
    '''
    Takes list of sqrs as strings matching subdirectories at http://ftp.geogratis.gc.ca/pub/nrcan_rncan/elevation/cdem_mnec/
    Returns list of urls to download zipped tifs contained in those squares
    '''
    ftp = ftputil.FTPHost(FTP_HOST,'anonymous','anonymous@domain.com')
    paths = []
    try:
        for square in sqrs:
            dir_ = os.path.join(FTP_DIR, square)
            recursive = ftp.walk(dir_,topdown=True,onerror=None)
            for root,dirs,files in recursive:
                for name in files:
                    path = FTP_HOST + os.path.join(root,name) 
                    path = "ftp://" + path
                    path = path.replace("\\", "/")
                    if path.endswith("tif.zip"):
                        print(path)
                        paths.append(path)
    except Exception as ex:
        raise ex
    finally:
        ftp.close()
        print("closed!")
    return paths



