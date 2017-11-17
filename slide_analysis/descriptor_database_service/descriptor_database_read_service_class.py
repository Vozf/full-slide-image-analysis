import numpy
from slide_analysis.utils import get_descriptor_class_by_name


class DescriptorDatabaseReadService:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as file:
            self.info_obj = DescriptorDatabaseReadService._load_obj(file).item()
            self.descriptors_array = DescriptorDatabaseReadService._load_obj(file)
            self.descriptor_class = get_descriptor_class_by_name(self.info_obj["descriptor_name"])
            self.descriptor_params = self.info_obj["descriptor_params"]
            self.length = self.info_obj["length"]
            if self.descriptor_class is None:
                raise RuntimeError("File is corrupted")

    def __len__(self):
        return self.length

    @staticmethod
    def _load_obj(file):
        return numpy.load(file)
