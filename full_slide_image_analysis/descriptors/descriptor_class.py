from full_slide_image_analysis.utils import Tile
import numpy


class Descriptor:
    def __init__(self, tile):
        self.tile = tile
        self._calc()
        return

    def _calc(self):
        tile = self.tile

        self.value = ''
        return

    def get_value(self):
        return self.value
