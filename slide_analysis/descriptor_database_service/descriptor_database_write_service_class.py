import os

import numpy


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

    @staticmethod
    def generate_name_of_basefile(base_path, image_path, descr_class, descr_params):
        image_name = os.path.basename(image_path)
        return base_path + descr_class.__name__ + " " + str(
            descr_params) + " " + image_name[0:image_name.find('.')] + ".npy"

    # todo move making of descr_filename somewhere else, so it can be accessed and modified
    def create(self, tile_stream):
        split = tile_stream.splitting_service
        image_path = split.path
        length = len(tile_stream)
        descr_filename = self.generate_name_of_basefile(self.base_path, image_path,
                                                        self.descriptor_class,
                                                        self.descriptor_params)

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        descr = self.descriptor_class(self.descriptor_params)
        info_obj = self.generate_database_info(image_path, length, split.tile_width,
                                               split.tile_height, split.step,
                                               split.width, split.height)

        descr_array = descr.get_descriptor_array(tile_stream)

        with open(descr_filename, 'wb') as file:
            self._dump_obj(file, info_obj)
            self._dump_obj(file, descr_array)

        return descr_filename

    def generate_database_info(self, image_path, length, tile_w, tile_h, step, img_w, img_h):
        return {
            "descriptor_name": self.descriptor_class.__name__,
            "descriptor_params": self.descriptor_params,
            "image_path": image_path,
            "length": length,
            "tile_width": tile_w,
            "tile_height": tile_h,
            "step": step,
            "img_width": img_w,
            "img_height": img_h
        }
