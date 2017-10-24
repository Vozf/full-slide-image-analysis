from slide_analysis.descriptors import all_descriptors
from slide_analysis.descriptor_database_service import DescriptorDatabaseWriteService
from slide_analysis.splitting_service import SplittingService


class Model:
    def __init__(self):
        self.descriptors = all_descriptors
        self.params = [None, (3, 2, 3)]

    def calculate_descriptors(self, idx, filepath, directory_path):
        split = SplittingService()
        stream = split.split_to_tiles(filepath)

        descriptor_database_serice =\
            DescriptorDatabaseWriteService(self.descriptors[idx], self.params[idx], directory_path)
        descriptor_database_serice.create(stream)
