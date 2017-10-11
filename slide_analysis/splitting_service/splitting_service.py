import openslide

import slide_analysis.splitting_service.constants as constants
from slide_analysis.utils.tile_class import Tile


class SplittingService:
    def __init__(self):
        self.tile_width = constants.BASE_TILE_WIDTH
        self.tile_height = constants.BASE_TILE_HEIGHT

    def _open_image(self, filename):
        slide = openslide.open_slide(filename)
        (self.width, self.height) = slide.dimensions
        img = slide.read_region((0, 0), 0, (self.width, self.height))
        self.img_data = img.getdata()

    def _cut_tile(self, x_coord, y_coord):
        return Tile(x_coord, y_coord, self.tile_width, self.tile_height,
                    [[self.img_data[x_coord + self.width * y_index + x_index]
                      for x_index in range(0, self.tile_width)]
                     for y_index in range(y_coord, y_coord + self.tile_height)])

    def split_to_tiles(self, filename):
        self._open_image(filename)

        # dimensions of resulting array of tiles
        num_rows = int(self.height / self.tile_height)
        num_cols = int(self.width / self.tile_width)

        return [[self._cut_tile(self.tile_width * col, self.tile_height * row)
                 for col in range(0, num_cols)]
                for row in range(0, num_rows)]
