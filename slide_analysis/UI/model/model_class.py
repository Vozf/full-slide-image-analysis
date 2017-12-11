import matplotlib.cm as cm
from threading import Thread

from slide_analysis.descriptor_database_service import DescriptorDatabaseWriteService
from slide_analysis.descriptors import all_descriptors
from slide_analysis.search_service import SearchService
from slide_analysis.similarities import all_similarities
from slide_analysis.splitting_service import SplittingService
from slide_analysis.search_service import SearchService


class Model:
    def __init__(self):
        self.descriptors = all_descriptors
        self.similarities = all_similarities

    def calculate_descriptors(self, descriptor_idx, descriptor_params, imagepath, directory_path):
        thread = Thread(target=self.calculate_descriptors_task,
                        args=(descriptor_idx, descriptor_params, imagepath, directory_path))
        thread.daemon = True
        thread.start()

    def calculate_descriptors_task(self, descriptor_idx, descriptor_params, imagepath, directory_path):
        split = SplittingService()
        stream = split.split_to_tiles(imagepath)

        descriptor_database_service = \
            DescriptorDatabaseWriteService(self.descriptors[descriptor_idx], descriptor_params,
                                           directory_path)
        descriptor_base = descriptor_database_service.create(stream)
        self.init_search_service(descriptor_base)

    def init_search_service(self, desc_path):
        self.search_service = SearchService(desc_path)

    def create_img_map(self, sim_map):
        map = cm.ScalarMappable(cmap='jet').to_rgba(sim_map, bytes=True)
        return map

    def find_similar(self, tile, n, similarity_class_idx, similarity_class_params):
        similarity_obj = self.search_service.search(tile, n, self.similarities[similarity_class_idx],
                                          similarity_class_params)
        sim_map = similarity_obj["sim_map"]
        return {
            "top_n": similarity_obj["top_n"],
            "img_arr": self.create_img_map(sim_map)
        }
