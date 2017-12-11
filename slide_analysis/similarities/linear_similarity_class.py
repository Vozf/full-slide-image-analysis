import numpy as np
from slide_analysis.descriptors import COLOR_RANGE


class LinearSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, descriptors_array, hist):
        distances = np.sum(np.abs(descriptors_array - hist), axis=1)
        return 1 - distances / (2 * COLOR_RANGE ** 2)
