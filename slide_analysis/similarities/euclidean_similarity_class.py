import numpy as np


class EuclideanSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, hist1, hist2):
        return 1 / (1 + np.linalg.norm(hist1 - hist2))

    def compare_arr_to_single(self, arr, hist):
        return 1 / (1 + np.linalg.norm(arr - hist, axis=1))
