import openslide

from slide_analysis.constants.tile import *
from slide_analysis.utils import Tile
from slide_analysis.utils.tile_stream_class import TileStream


class SplittingService:
    def __init__(self):
        self.tile_width = BASE_TILE_WIDTH
        self.tile_height = BASE_TILE_HEIGHT
        self.step = BASE_STEP

    def _open_image(self, path):
        self.path = path
        self.slide = openslide.open_slide(path)
        (self.width, self.height) = self.slide.level_dimensions[0]
        self.num_rows = int(self.height / self.step)
        self.num_cols = int(self.width / self.step)

    def _get_params_for_cut(self, index):
        row = int(index / self.num_rows)
        column = index - row * self.num_rows
        y_coord = row * self.step
        x_coord = column * self.step
        return x_coord, y_coord

    def _cut_tile_by_coord(self, x_coord, y_coord):
        ret = Tile(x_coord, y_coord, self.tile_width, self.tile_height,
                    self.slide.read_region((x_coord, y_coord), 0,
                                           (self.tile_width, self.tile_height)).getdata())
        return ret

    def _cut_tile(self, index):
        params = self._get_params_for_cut(index)
        return self._cut_tile_by_coord(params[0], params[1])

    def split_to_tiles(self, path):
        self._open_image(path)
        return TileStream(self)

    def __len__(self):
        return self.num_rows * self.num_cols
