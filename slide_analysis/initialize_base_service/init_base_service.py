from slide_analysis.descriptors import HistogramDescriptor
from slide_analysis.initialize_base_service.splitting_service import SplittingService
from slide_analysis.initialize_base_service.tile_stream_class import TileStream
from slide_analysis.utils import Tile
import openslide
import os


class InitBaseService:
    def __init__(self, path):
        self.base_path = path
        self.splitting_service = SplittingService()
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_to_file(self, file, descr):
        file.write(str(descr.tile.x) + '%' + str(descr.tile.y) + '%'
                   + str(descr.tile.width) + '%' + str(descr.tile.height) + '%'
                   + str(descr.get_value())[1:-1] + '\n')

    def init_base(self, filename, descriptor_params):
        dirname = filename[0:filename.find('.')]
        if not os.path.exists(self.base_path + '/' + dirname + '/Histogram'):
            os.makedirs(self.base_path + '/' + dirname + '/Histogram')

        slide = openslide.open_slide(filename)
        print(slide)
        tile_stream = self.splitting_service.split_to_tiles(slide)
        while tile_stream.has_next():
            descr = HistogramDescriptor(descriptor_params)
            descr.set_tile(tile_stream.next())
            descr.get_value()
            file = open(self.base_path + '/' + dirname + '/Histogram/' + str(descr.tile.x) + '%' + str(descr.tile.y) + '%'
                        + str(descr.tile.width) + '%' + str(descr.tile.height) + '%', 'w')
            self.write_to_file(file, descr)
            file.close()


inb = InitBaseService('initialize_base_service')
inb.init_base("test.tif", (3, 2, 3))
