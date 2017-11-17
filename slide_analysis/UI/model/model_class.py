from slide_analysis.descriptors import all_descriptors
from slide_analysis.similarities import all_similarities
from slide_analysis.descriptor_database_service import DescriptorDatabaseWriteService
from slide_analysis.splitting_service import SplittingService
from slide_analysis.search_service import SearchService


class Model:
    def __init__(self):
        self.descriptors = all_descriptors
        self.similarities = all_similarities

    def calculate_descriptors(self, descriptor_idx, descriptor_params, imagepath, directory_path):
        split = SplittingService()
        stream = split.split_to_tiles(imagepath)

        descriptor_database_service = \
            DescriptorDatabaseWriteService(self.descriptors[descriptor_idx], descriptor_params,
                                           directory_path)
        return descriptor_database_service.create(stream)

    def init_search_service(self, desc_path):
        self.search_service = SearchService(desc_path)

    def find_similar(self, tile, n, similarity_class_idx, similarity_class_params):
        return self.search_service.search(tile, n, self.similarities[similarity_class_idx],
                                               similarity_class_params)