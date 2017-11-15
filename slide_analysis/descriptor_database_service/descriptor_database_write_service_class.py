import os
import pickle
import datetime
import numpy
from slide_analysis.utils import compose, get_descriptor_class_by_name, DescriptorDump


class DescriptorDatabaseWriteService:
    def __init__(self, descriptor_class, descriptor_params, path_to_descriptors):
        self.descriptor_class = descriptor_class
        self.descriptor_params = descriptor_params

        if path_to_descriptors[-1] == '/':
            self.base_path = path_to_descriptors
        else:
            self.base_path = path_to_descriptors + '/'

    @staticmethod
    def _dump_obj(file, obj):
        return numpy.save(file, obj)

    def create(self, tile_stream):
        image_path = tile_stream.splitting_service.path
        length = len(tile_stream)

        image_name = os.path.basename(image_path)

        descr_filename = self.base_path + str(datetime.datetime.now()).split('.')[
            0] + " " + self.descriptor_class.__name__ + " " + str(
            self.descriptor_params) + " " + image_name[0:image_name.find('.')] + ".npy"

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        descr = self.descriptor_class(self.descriptor_params)

        info_obj = self.generate_database_info(image_path, length)

        with open(descr_filename, 'wb') as file:
            self._dump_obj(file, info_obj)
            self._dump_obj(file, descr.get_descriptor_array(tile_stream))

        return descr_filename

    def generate_database_info(self, image_path, length):
        return {
            "descriptor_name": self.descriptor_class.__name__,
            "descriptor_params": self.descriptor_params,
            "image_path": image_path,
            "length": length
        }

    @staticmethod
    def from_database_example(path):
        with open(path, 'rb') as file:
            info_obj = pickle.load(file)

            descriptor_class = get_descriptor_class_by_name(info_obj["descriptor_name"])
            descriptor_params = info_obj["descriptor_params"]
            path_to_descriptors = path.abspath(path.join(info_obj["image_path"], "../.."))
            if descriptor_class is None:
                return None

            return DescriptorDatabaseWriteService(descriptor_class,
                                                  descriptor_params, path_to_descriptors)

    @staticmethod
    def generate_dump_obj(descr):
        def generate_dump_obj_util(tile):
            return DescriptorDump(tile.x, tile.y, tile.height, tile.width, descr.calc(tile))

        return generate_dump_obj_util
