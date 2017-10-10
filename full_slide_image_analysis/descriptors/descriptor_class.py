from full_slide_image_analysis.utils import Tile


class Descriptor:
    def __init__(self, tile):
        self.tile = tile
        self._calc()

    def _calc(self):
        tile = self.tile

        self.value = ''

    def get_value(self):
        return self.value
