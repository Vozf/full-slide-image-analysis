import numpy as np


class EuclideanSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, arr, hist):
        return 1 / (1 + np.linalg.norm(arr - hist, axis=1))
