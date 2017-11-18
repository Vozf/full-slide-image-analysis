import numpy as np


class Chi2Similarity:
    def __init__(self, eps):
        self.eps = eps

    def compare(self, descriptors_array, hist):
        distance = 0.5 * np.sum(
            (descriptors_array - hist) ** 2 / (descriptors_array + hist + self.eps), axis=1)

        return 1 / (1 + distance)
