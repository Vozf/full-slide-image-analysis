import numpy as np


class EuclideanSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, descriptors_array, hist):
        return 1 / (1 + np.linalg.norm(descriptors_array - hist, axis=1))
