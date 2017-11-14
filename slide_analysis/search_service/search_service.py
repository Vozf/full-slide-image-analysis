from slide_analysis.descriptor_database_service.descriptor_database_read_service_class import \
    DescriptorDatabaseReadService
from slide_analysis.search_service.top_n_list_class import TopNList


class SearchService:
    def __init__(self, desc_path):
        ddrs = DescriptorDatabaseReadService(desc_path)
        self.tile_descriptor_class = ddrs.descriptor_class(ddrs.descriptor_params)
        self.stream = ddrs.get_descriptor_stream()
        self.info_obj = self.stream.next()

    def search(self, tile, n, similarity_class, similarity_class_params):
        top_n = TopNList(n)
        tile_descriptor = self.tile_descriptor_class.calc(tile)
        tile_similarity = similarity_class(similarity_class_params)

        self.stream.for_each(
            lambda descriptor_dump: top_n.update(
                element=(tile_similarity.compare(tile_descriptor, descriptor_dump.descriptor),
                         descriptor_dump)))

        return top_n

