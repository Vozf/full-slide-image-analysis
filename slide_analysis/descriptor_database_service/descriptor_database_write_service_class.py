import os
import pickle
from slide_analysis.utils import compose, get_descriptor_class_by_name


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
        return pickle.dump(obj, file)

    def create(self, tile_stream):
        image_path = tile_stream.splitting_service.path
        length = len(tile_stream)

        image_name = os.path.basename(image_path)

        descr_path = self.base_path + image_name[0:image_name.find('.')] + '/' + self.descriptor_class.__name__ + '/'
        descr_filename = descr_path + str(self.descriptor_params) + '.bin'
        print(descr_filename)

        if not os.path.exists(descr_path):
            os.makedirs(descr_path)

        descr = self.descriptor_class(self.descriptor_params)

        info_obj = self.generate_database_info(image_path, length)

        with open(descr_filename, 'wb') as file:
            self._dump_obj(file, info_obj)
            tile_stream.for_each(compose(
                lambda descriptor: self._dump_obj(file, descriptor),
                descr.calc))

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