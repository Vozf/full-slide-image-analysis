class Tile:
    def __init__(self, x, y, width, height, pixel_array):

        # init tile params: coordinates of
        # left-top corner, dimensions and
        # (r, g, b, a) values of pixels on it
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pixel_array = pixel_array
