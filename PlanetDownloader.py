# planet downloader
from osgeo import gdal
from requests.auth import HTTPBasicAuth
import os
import requests
import sys
from subprocess import run

class PlanetDownloader:

    def __init__(self, input_file, clip_file):
        self.download_urls = []


        with open(input_file) as f:
            for each_link in f.readline():
                self.download_urls.append(each_id)

        item_type = "PSScene4Band"
        asset_type = "analytic"
        item_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'.format(item_type, item_id)
        
    def download(self):
        os.makedirs("tmp_images")

        count = 0
        for i in download_urls:
            vsicurl_url = '/vsicurl/' + i
            output_file = 'tmp_images/' + item_id +  '_subarea' + str(count) + '.tif'
            count += 1

            # GDAL Warp crops the image by our AOI, and saves it
            gdal.Warp(output_file, vsicurl_url, dstSRS = 'EPSG:4326', cutlineDSName = clip_file, cropToCutline = True)
            
        

if __name__ == "__main__":
    input_file, merged_file, clip_file = sys.argv
    d = PlanetDownloader(input_file, clip_file)
    d.download()
    # merge files and then move the temporary directory
    run("rio tmp_images/*.tif " + merged_file + ".tif")
    run("mv tmp_images " + merged_file+"_imgs")

    
