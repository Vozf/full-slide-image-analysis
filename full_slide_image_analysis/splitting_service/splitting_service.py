import openslide
import full_slide_image_analysis.splitting_service.constants as constants
from full_slide_image_analysis.utils import Tile
from full_slide_image_analysis.utils import TileStream


class SplittingService:
    def __init__(self):
        self.tile_width = constants.BASE_TILE_WIDTH
        self.tile_height = constants.BASE_TILE_HEIGHT
        self.step = constants.BASE_STEP

    def _open_image(self, filename):
        self.slide = openslide.open_slide(filename)
        (self.width, self.height) = self.slide.level_dimensions[0]
        self.num_rows = int(self.height / self.step)
        self.num_cols = int(self.width / self.step)

    def _get_params_for_cut(self, index):
        row = int(index / self.num_rows)
        column = index - row * self.num_rows
        x_coord = row * self.step
        y_coord = column * self.step
        return x_coord, y_coord

    def _cut_tile(self, x_coord, y_coord):
        return Tile(x_coord, y_coord, self.tile_width, self.tile_height,
                    self.slide.read_region((x_coord, y_coord), 0,
                                           (self.tile_width, self.tile_height)).getdata())

    def cut_tile(self, index):
        params = self._get_params_for_cut(index)
        self._cut_tile(params[0], params[1])

    def split_to_tiles(self, filename):
        self._open_image(filename)
        return TileStream(self.cut_tile, self.num_rows * self.num_cols)
