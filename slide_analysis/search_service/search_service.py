from slide_analysis.descriptor_database_service.descriptor_database_read_service_class import \
    DescriptorDatabaseReadService
import numpy
from slide_analysis.utils.functions import get_tiles_coords_from_indexes


class SearchService:
    def __init__(self, desc_path):
        ddrs = DescriptorDatabaseReadService(desc_path)
        self.tile_descriptor_class = ddrs.descriptor_class(ddrs.descriptor_params)
        self.info_obj = ddrs.info_obj
        self.descriptors_array = ddrs.descriptors_array

    def convert_to_tile_coords(self, indexes):
        return get_tiles_coords_from_indexes(indexes,
                                          self.info_obj['step'],
                                          self.info_obj['img_width'])

    def search(self, tile, n, similarity_class, similarity_class_params):
        tile_descriptor = self.tile_descriptor_class.calc(tile)
        tile_similarity = similarity_class(similarity_class_params)
        distances = tile_similarity.compare(self.descriptors_array,
                                            tile_descriptor)
        indexes = numpy.argsort(-distances)

        return self.convert_to_tile_coords(indexes[0: n])
