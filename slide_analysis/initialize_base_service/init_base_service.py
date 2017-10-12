from slide_analysis.descriptors import HistogramDescriptor
from slide_analysis.splitting_service import SplittingService
from slide_analysis.utils import Tile, TileStream
import os


class InitBaseService:
    def __init__(self, path):
        self.base_path = path
        self.splitting_service = SplittingService()
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_to_file(self, file, descr):
        file.write(descr.val)

    def init_base(self, filename, descriptor_type, descriptor_params):
        dirname = filename[0:filename.find('.')]
        if not os.path.exists(self.base_path + '/' + dirname):
            os.mkdir(self.base_path + '/' + dirname)

        os.chdir(self.base_path + '/' + dirname)
        if descriptor_type == 'Histogram':
            if not os.path.exists(os.getcwd() + '/Histogram'):
                os.mkdir(os.getcwd() + '/Histogram')

            os.chdir(os.getcwd() + '/Histogram')
            file = open(os.getcwd() + '/descr.txt', 'w')

            tile_stream = self.splitting_service.split_to_tiles(filename)
            while tile_stream.has_next():
                descr = HistogramDescriptor(descriptor_params)
                descr.set_tile(tile_stream.next())
                file.write(str(descr.get_value())[1:-1] + '\n')

            file.close()
