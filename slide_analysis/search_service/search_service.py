from slide_analysis.descriptor_database_service.descriptor_database_read_service_class import \
    DescriptorDatabaseReadService
from slide_analysis.search_service.top_n_list_class import TopNList
import numpy
from slide_analysis.utils.functions import get_tile_coords_from_index


class SearchService:
    def __init__(self, desc_path):
        ddrs = DescriptorDatabaseReadService(desc_path)
        self.tile_descriptor_class = ddrs.descriptor_class(ddrs.descriptor_params)
        self.info_obj = ddrs.info_obj
        self.descriptors_array = ddrs.descriptors_array

    def convert_to_tile_coords(self, indexes):
        return get_tile_coords_from_index(indexes,
                                          self.info_obj['tile_width'],
                                          self.info_obj['tile_height'],
                                          self.info_obj['step'],
                                          self.info_obj['img_width'],
                                          self.info_obj['img_height'])

    def search(self, tile, n, similarity_class, similarity_class_params):
        top_n = TopNList(n)
        tile_descriptor = self.tile_descriptor_class.calc(tile)
        tile_similarity = similarity_class(similarity_class_params)
        distances = tile_similarity.compare_arr_to_single(self.descriptors_array,
                                                          tile_descriptor)
        indexes = numpy.argsort(-distances)

        return self.convert_to_tile_coords(indexes[0: n])
