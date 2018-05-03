#!/usr/bin/env python

# This creates a bounding box and chunks it out into smaller, symmetrical boxes in geojson


# Class bones taken from https://github.com/Luqqk/geojson-bbox
import json
import os
import re
import numpy as np
from itertools import product
from subprocess import run

from settings import TRIM_LEVEL
from settings import GEOJSON_DIRECTORY
from shapely.geometry import Polygon
from geopandas import GeoDataFrame
from settings import CHUNK_DIR
from settings import NUMBER_OF_CHUNKS

trim_1m = lambda x: round(x, TRIM_LEVEL) # roughly 1m precision

class GeoJSONBoundBox:
    """GeoJSON class which allows to calculate bbox"""
    def __init__(self, geojson_file):

        self.geojson_root = re.findall(r'(\S+).geojson', str(geojson_file))[0]
        #print(self.geojson_root)

        with open(GEOJSON_DIRECTORY + geojson_file) as f:
             self.geojson = json.load(f)
        if self.geojson['type'] == 'FeatureCollection':
            self.coords = list(self._flatten([f['geometry']['coordinates']
                           for f in self.geojson['features']]))
            self.features_count = len(self.geojson['features'])
        elif self.geojson['type'] == 'Feature':
            self.coords = list(self._flatten([
                        self.geojson['geometry']['coordinates']]))
            self.features_count = 1
        else:
            self.coords = list(self._flatten([self.geojson['coordinates']]))
            self.features_count = 1

    def _flatten(self, l):
        for val in l:
            if isinstance(val, list):
                for subval in self._flatten(val):
                    yield subval
            else:
                yield val

    def bbox(self):
        return [min(self.coords[::2]), min(self.coords[1::2]),
                max(self.coords[::2]), max(self.coords[1::2])]

    def chunk_bbox(self, pieces=None):
        assert pieces % 2 == 0, "Pieces must be even"


        sub_areas = []
        bbox_vals = self.bbox()
        set1 = np.linspace(bbox_vals[0], bbox_vals[2], pieces*2)
        set2 = np.linspace(bbox_vals[1], bbox_vals[3], pieces*2)

        #from geojson import FeatureCollection
        count = 0
        for i in pair_wise_iterator(set1):
            for j in pair_wise_iterator(set2):

                # truncate the coordinates
                box = [(trim_1m(x),trim_1m(y)) for x,y in product(i,j)]

                box = make_line_ordered(box)

                # add the beginning value to the end, per geojson specificiation
                box.append(box[0])
                # create a dataframe and use it to write to a shapefile
                poly_df = GeoDataFrame(geometry=[Polygon(box)])

                file_name = CHUNK_DIR + self.geojson_root + str(count)
                with open(file_name + ".geojson", 'w') as f:
                    f.write(poly_df.to_json())
                count += 1
        print("Chunking Complete\n")

def make_line_ordered(coord_list):
    coord_list.sort()

    rv = coord_list[:2] # will be sorted on x's
    coord_list.remove(rv[0])
    coord_list.remove(rv[1])

    for i in coord_list:
        if i[1] == rv[-1][1]:
            rv.append(i)
            coord_list.remove(i)
    rv.append(coord_list[0])
    return rv


def pair_wise_iterator(x_set):
    for x_index in range(len(x_set)):
        if x_index % 2 != 0:
            yield x_set[x_index], x_set[x_index-1]



if __name__ == "__main__":

    os.makedirs(CHUNK_DIR)

    for i in os.listdir(GEOJSON_DIRECTORY):
        if ".geojson" not in i:
            continue
        bbox = GeoJSONBoundBox(i)
        bbox.chunk_bbox(NUMBER_OF_CHUNKS)