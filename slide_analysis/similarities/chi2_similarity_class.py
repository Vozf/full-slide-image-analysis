import numpy as np

from slide_analysis.descriptors import COLOR_RANGE


class Chi2Similarity:
    def __init__(self, eps):
        self.eps = eps

    def compare(self, descriptors_array, hist):
        distances = 0.5 * np.sum((descriptors_array - hist) ** 2 / (descriptors_array + hist + self.eps), axis=1)

        return 1 - distances / (np.sqrt(2) * COLOR_RANGE ** 2)
