import numpy as np
from slide_analysis.descriptors import COLOR_RANGE


class EuclideanSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, descriptors_array, hist):
        distances = np.linalg.norm(descriptors_array - hist, axis=1)
        return 1 - distances / (np.sqrt(2) * COLOR_RANGE ** 2)
