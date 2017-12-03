import numpy

from slide_analysis.descriptor_database_service import DescriptorDatabaseWriteService
from slide_analysis.descriptors import all_descriptors
from slide_analysis.search_service import SearchService
from slide_analysis.similarities import all_similarities
from slide_analysis.splitting_service import SplittingService


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

    def create_img_arr(self, sim_map):
        print(' ----------- CREATING IMG ARR --------------')
        shape = sim_map.shape
        img_arr = numpy.empty([shape[0], shape[1], 3], dtype=numpy.uint8)

        for i in numpy.arange(0, shape[0]):
            for j in numpy.arange(0, shape[1]):
                img_arr[i][j][0] = 255 * sim_map[i][j]
                img_arr[i][j][1] = 0
                img_arr[i][j][2] = 255 * (1 - sim_map[i][j])

        return img_arr.reshape([shape[0], shape[1], 3])

    def find_similar(self, tile, n, similarity_class_idx, similarity_class_params):
        similarity_obj = self.search_service.search(tile, n,
                                                    self.similarities[similarity_class_idx],
                                                    similarity_class_params)
        sim_map = similarity_obj["sim_map"]
        return {
            "top_n": similarity_obj["top_n"],
            "img_arr": self.create_img_arr(sim_map)
        }
