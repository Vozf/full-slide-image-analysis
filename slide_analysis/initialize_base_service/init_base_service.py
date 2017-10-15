import os
import pickle

import openslide

from slide_analysis.descriptors import HistogramDescriptor
from slide_analysis.splitting_service.splitting_service import SplittingService


class InitBaseService:
    def __init__(self, path):
        if path[-1] == '/':
            self.base_path = path
        else:
            self.base_path = path + '/'
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_to_file(self, tile):
        descr = self.descriptor_class(self.descriptor_params)
        descr.calc_by_tile(tile)
        pickle.dump(descr, self.opened_descr_file)

    def init_base(self, tile_stream, descriptor_class, descriptor_params, imagename, classname):
        self.tile_stream = tile_stream
        self.descriptor_class = descriptor_class
        self.descriptor_params = descriptor_params
        self.descr_path = self.base_path + imagename[0:imagename.find('.')] + '/' + classname + '/'
        self.descr_filename = self.descr_path + str(descriptor_params) + '.bin'
        if not os.path.exists(self.descr_path):
            os.makedirs(self.descr_path)

        with open(self.descr_filename, 'wb') as file:
            self.opened_descr_file = file
            self.tile_stream.for_each(self.write_to_file)
