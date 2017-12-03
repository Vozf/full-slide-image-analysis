import openslide
import time
from PIL import ImageQt
from PIL import Image

from slide_analysis.UI.view.constants import BASE_SCALE_FACTOR, SCALE_MULTIPLIER
from slide_analysis.constants.tile import BASE_TILE_WIDTH, BASE_TILE_HEIGHT


class ImageHelper:
    def __init__(self, filepath):
        self.filepath = filepath
        self.openslide_image = openslide.OpenSlide(filepath)
        self.current_level = self.openslide_image.level_count - 1
        self.level_dimensions = self.openslide_image.level_dimensions
        self.current_displayed_image_coordinates = (0, 0)
        self.current_image_coordinates = self.current_displayed_image_coordinates

        self.current_displayed_image_size = self.level_dimensions[self.current_level]
        self.current_image_size = self.current_displayed_image_size

        self.image_dimensions = self.level_dimensions[0]
        self.scale_factor = BASE_SCALE_FACTOR
        self.current_movement_step = (self.image_dimensions[0] // self.scale_factor,
                                      self.image_dimensions[1] // self.scale_factor)
        self.image = self.openslide_image.read_region(self.current_image_coordinates, self.current_level,
                                                      self.level_dimensions[self.current_level])
        self.image_slide = openslide.ImageSlide(self.image)
        self.print_status()

    def get_filepath(self):
        return self.filepath

    def get_tile_coordinates(self, mouse_pos_point):
        actual_coordianates_x = int((mouse_pos_point.x()) * pow(2, self.current_level) + self.current_image_coordinates[0])
        actual_coordianates_y = int((mouse_pos_point.y()) * pow(2, self.current_level) + self.current_image_coordinates[1])
        print('User selected tile coordinates: ', actual_coordianates_x, actual_coordianates_y)
        actual_coordianates = (actual_coordianates_x, actual_coordianates_y)

        if actual_coordianates[0] >= 0 and actual_coordianates[1] >= 0:
            return actual_coordianates
        else:
            return 0, 0

    def get_qt_from_coordinates(self, tile_coordinates):
        return ImageQt.ImageQt(self.openslide_image.read_region(tile_coordinates, 0, (
        BASE_TILE_WIDTH, BASE_TILE_HEIGHT)))

    def img_from_arr(self, arr):
        print("---------- CREATING IMG FROM ARR -------------")
        shape = arr.shape
        return Image.fromarray(arr.reshape([shape[1], shape[0], shape[2]]), 'RGB')

    def __calculate_movement_step_coordinates(self):
        self.current_movement_step = (self.image_dimensions[0] // self.scale_factor,
                                      self.image_dimensions[1] // self.scale_factor)
        print('Current movement step:', self.current_movement_step)

    def set_current_image_rect(self, view_rect):
        self.current_displayed_image_size = (int(view_rect.width()), int(view_rect.height()))
        self.current_displayed_image_coordinates = (
            self.current_image_coordinates[0] + view_rect.x() * pow(2, self.current_level),
            self.current_image_coordinates[1] + view_rect.y() * pow(2, self.current_level))

    def update_q_image(self, viewrect=None):
        if viewrect is not None:
            factor = min(viewrect[0] / self.current_displayed_image_size[0],
                         viewrect[1] / self.current_displayed_image_size[1])
            if factor > 1.25:
                self.move_to_next_image_level()
        self.image = self.openslide_image.read_region(self.current_image_coordinates, self.current_level,
                                                      self.current_image_size)
        self.print_status()
        return ImageQt.ImageQt(self.image)

    def update_image_rect(self):
        offset = (self.current_displayed_image_size[0] * pow(2, self.current_level),
                  self.current_displayed_image_size[1] * pow(2, self.current_level))

        print(offset)
        print('previous')
        print(self.current_displayed_image_coordinates)
        print(self.current_displayed_image_size)
        print(self.current_image_coordinates)
        print(self.current_image_size)

        self.current_image_coordinates = (
            int(self.current_displayed_image_coordinates[0] - offset[0]),
            int(self.current_displayed_image_coordinates[1] - offset[1]))

        if self.current_image_coordinates[0] < 0:
            self.current_image_coordinates = (0, self.current_image_coordinates[1])

        if self.current_image_coordinates[1] < 0:
            self.current_image_coordinates = (self.current_image_coordinates[0], 0)

        self.current_image_size = (
            self.current_displayed_image_size[0] * 3,
            self.current_displayed_image_size[1] * 3)

        current_image_size = self.get_current_image_size()
        if self.current_image_size[0] > current_image_size[0]:
            self.current_image_size = (current_image_size[0], self.current_image_size[1])

        if self.current_image_size[1] > current_image_size[1]:
            self.current_image_size = (self.current_image_size[0], current_image_size[1])

        print('current')
        print(self.current_displayed_image_coordinates)
        print(self.current_displayed_image_size)
        print(self.current_image_coordinates)
        print(self.current_image_size)
        print('\n')

    def get_q_image(self):
        return ImageQt.ImageQt(self.image)

    def get_current_image_size(self):
        return self.level_dimensions[self.current_level]

    def move_to_next_image_level(self):
        if self.current_level != 0:
            self.current_level -= 1
            self.current_displayed_image_size = (
                self.current_displayed_image_size[0] * 2, self.current_displayed_image_size[1] * 2)
            self.update_image_rect()
            self.image = self.openslide_image.read_region(self.current_image_coordinates,
                                                          self.current_level,
                                                          self.current_image_size)

    def get_scale_factor(self):
        return max(self.current_image_size[0] / self.current_displayed_image_size[0],
                   self.current_image_size[1] / self.current_displayed_image_size[1])

    def get_current_displayed_image_rect(self):
        return ((self.current_displayed_image_coordinates[0] - self.current_image_coordinates[0]) // pow(2, self.current_level),
                (self.current_displayed_image_coordinates[1] - self.current_image_coordinates[1]) // pow(2, self.current_level),
                self.current_displayed_image_size[0],
                self.current_displayed_image_size[1])

    def move_to_prev_image_level(self):
        if self.current_level != self.openslide_image.level_count - 1:
            self.current_level += 1
            self.current_displayed_image_size = (
                self.current_displayed_image_size[0] // 2, self.current_displayed_image_size[1] // 2)
            self.update_image_rect()
            self.image = self.openslide_image.read_region(self.current_image_coordinates,
                                                          self.current_level,
                                                          self.current_image_size)

    def set_coordinates(self, x, y):
        to_set_x = self.__get_correct_coordinate(x, self.image_dimensions[0],
                                                 self.current_movement_step[1])
        to_set_y = self.__get_correct_coordinate(y, self.image_dimensions[1],
                                                 self.current_movement_step[1])
        self.current_displayed_image_coordinates = (to_set_x, to_set_y)
        self.print_status()

    @staticmethod
    def __get_correct_coordinate(coordinate, dimension, step):
        if coordinate > 0:
            if coordinate < dimension:
                return coordinate
            else:
                return dimension - step
        else:
            return 0

    def print_status(self):
        print('Current level:', self.current_level)
        print('Level dimensions:', self.current_displayed_image_size)
        print('Coordinates:', self.current_displayed_image_coordinates)
        print('\n')
