import pickle
from slide_analysis.utils import get_descriptor_class_by_name, DescriptorStream


class DescriptorDatabaseReadService:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as file:
            info_obj = DescriptorDatabaseReadService._load_obj(file)
            self.descriptor_class = get_descriptor_class_by_name(info_obj["descriptor_name"])
            self.descriptor_params = info_obj["descriptor_params"]
            self.length = info_obj["length"]
            if self.descriptor_class is None:
                raise RuntimeError("File is corrupted")

    def __len__(self):
        return self.length

    @staticmethod
    def _load_obj(file):
        return pickle.load(file)

    def get_descriptor_stream(self):
        return DescriptorStream(self)
