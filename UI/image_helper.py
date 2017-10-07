import sys
from PySide import QtGui
import openslide

sys.modules['PyQt5.QtGui'] = QtGui
from PIL import ImageQt


class ImageHelper:
    def __init__(self, file_name):
        self.openslide_image = openslide.OpenSlide(file_name)
        self.current_level = self.openslide_image.level_count - 1
        self.level_dimensions = self.openslide_image.level_dimensions
        self.current_coordinates = (0, 0)
        self.image_dimensions = self.level_dimensions[0]
        self.scale_factor = 1
        self.current_movement_step = (self.image_dimensions[0] / self.scale_factor,
                                      self.image_dimensions[1] / self.scale_factor)
        self.current_window_size = self.level_dimensions[self.current_level]
        self.image = self.openslide_image.read_region(self.current_coordinates, self.current_level,
                                                      self.level_dimensions[self.current_level])
        self.image_slide = openslide.ImageSlide(self.image)
        print self.image_slide.level_downsamples
        print self.current_level
        print self.level_dimensions

    def __calculate_movement_step_coordinates(self):
        self.current_movement_step = (self.image_dimensions[0] / self.scale_factor,
                                      self.image_dimensions[1] / self.scale_factor)

    def get_q_image(self):

        self.image = self.openslide_image.read_region(self.current_coordinates, self.current_level,
                                                      self.current_window_size)
        print self.current_coordinates, self.current_level, self.current_window_size
        return ImageQt.ImageQt(self.image)

    def change_image_properties(self, coordinates, level, size):
        self.current_coordinates = coordinates
        self.current_level = level
        self.current_window_size = size
        self.image = self.openslide_image.read_region(coordinates, self.current_level, size)
        return ImageQt.ImageQt(self.image)

    # Zooming is just moving to next level of image
    def zoom_in(self):
        if self.current_level != 0:
            self.current_level = self.current_level - 1
            self.scale_factor *= 2
            self.__calculate_movement_step_coordinates()
        return self.change_image_properties(self.current_coordinates, self.current_level,
                                            self.current_window_size)

    def zoom_out(self):
        if self.current_level < self.openslide_image.level_count - 1:
            self.current_level = self.current_level + 1
            self.scale_factor /= 2
            self.__calculate_movement_step_coordinates()
        return self.change_image_properties(self.current_coordinates, self.current_level,
                                            self.current_window_size)

    # TODO look at openslide library http://openslide.org/api/python/#module-openslide
    def move_right(self):
        if (self.current_coordinates[0] + 2 * self.current_movement_step[0]) <= \
                self.image_dimensions[0]:
            self.current_coordinates = (self.current_coordinates[0] + self.current_movement_step[0],
                                        self.current_coordinates[1])
            print self.level_dimensions[self.current_level]
            print self.current_coordinates

    def move_left(self):
        if self.current_coordinates[0] - self.current_movement_step[0] >= 0:
            self.current_coordinates = (self.current_coordinates[0] - self.current_movement_step[0],
                                        self.current_coordinates[1])
            print self.level_dimensions[self.current_level]
            print self.current_coordinates

    def move_down(self):
        if (self.current_coordinates[1] + 2 * self.current_movement_step[1]) <= \
                self.image_dimensions[1]:
            self.current_coordinates = (
                self.current_coordinates[0],
                self.current_coordinates[1] + self.current_movement_step[1])
            print self.level_dimensions[self.current_level]
            print self.current_coordinates

    def move_up(self):
        if self.current_coordinates[1] - self.current_movement_step[1] >= 0:
            self.current_coordinates = (
                self.current_coordinates[0],
                self.current_coordinates[1] - self.current_movement_step[1])
            print self.level_dimensions[self.current_level]
            print self.current_coordinates
