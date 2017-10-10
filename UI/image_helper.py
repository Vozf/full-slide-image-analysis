import openslide

from PIL import ImageQt

from UI.constants import BASE_SCALE_FACTOR, SCALE_MULTIPLIER


class ImageHelper:
    def __init__(self, file_name):
        self.openslide_image = openslide.OpenSlide(file_name)
        self.current_level = self.openslide_image.level_count - 1
        self.level_dimensions = self.openslide_image.level_dimensions
        self.current_coordinates = (0, 0)
        self.image_dimensions = self.level_dimensions[0]
        self.scale_factor = BASE_SCALE_FACTOR
        self.current_movement_step = (self.image_dimensions[0] // self.scale_factor,
                                      self.image_dimensions[1] // self.scale_factor)
        self.current_window_size = self.level_dimensions[self.current_level]
        self.image = self.openslide_image.read_region(self.current_coordinates, self.current_level,
                                                      self.level_dimensions[self.current_level])
        self.image_slide = openslide.ImageSlide(self.image)
        print (self.image_dimensions)
        self.print_status()

    def __calculate_movement_step_coordinates(self):
        self.current_movement_step = (self.image_dimensions[0] // self.scale_factor,
                                      self.image_dimensions[1] // self.scale_factor)
        print ('Current movement step:', self.current_movement_step)

    def get_q_image(self):
        self.image = self.openslide_image.read_region(self.current_coordinates, self.current_level,
                                                      self.current_window_size)
        self.print_status()
        return ImageQt.ImageQt(self.image)

    def change_image_properties(self):
        self.image = self.openslide_image.read_region(self.current_coordinates,
                                                      self.current_level, self.current_window_size)
        return ImageQt.ImageQt(self.image)

    # Zooming is just moving to next level of image
    def zoom_in(self):
        if self.current_level != 0:
            self.current_level = self.current_level - 1
            self.scale_factor *= SCALE_MULTIPLIER
            self.__calculate_movement_step_coordinates()
        return self.change_image_properties()

    def zoom_out(self):
        if self.current_level < self.openslide_image.level_count - 1:
            self.current_level = self.current_level + 1
            self.scale_factor //= SCALE_MULTIPLIER
            self.__calculate_movement_step_coordinates()
        return self.change_image_properties()

    def move_right(self):
        self.set_coordinates(self.current_coordinates[0] + self.current_movement_step[0],
                             self.current_coordinates[1])

    def move_left(self):
        self.set_coordinates(self.current_coordinates[0] - self.current_movement_step[0],
                             self.current_coordinates[1])

    def move_down(self):
        self.set_coordinates(self.current_coordinates[0],
                             self.current_coordinates[1] + self.current_movement_step[1])

    def move_up(self):
        self.set_coordinates(self.current_coordinates[0],
                             self.current_coordinates[1] - self.current_movement_step[1])

    def set_coordinates(self, x, y):
        to_set_x = self.__get_correct_coordinate(x, self.image_dimensions[0],
                                                 self.current_movement_step[1])
        to_set_y = self.__get_correct_coordinate(y, self.image_dimensions[1],
                                                 self.current_movement_step[1])
        self.current_coordinates = (to_set_x, to_set_y)
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
        print ('Current level:', self.current_level)
        print ('Level dimensions:', self.current_window_size)
        print ('Coordinates:', self.current_coordinates)
        print ('\n')
