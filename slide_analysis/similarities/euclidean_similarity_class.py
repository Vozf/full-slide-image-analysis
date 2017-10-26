import numpy as np


class EuclideanSimilarity:
    def __init__(self, fictive_param):
        pass

    def compare(self, hist1, hist2):
        return 1 / (1 + np.linalg.norm(hist1 - hist2))
