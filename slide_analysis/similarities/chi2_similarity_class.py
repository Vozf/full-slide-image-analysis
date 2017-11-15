import numpy as np


class Chi2Similarity:
    def __init__(self, eps):
        self.eps = eps

    def compare(self, hist1, hist2):
        distance = 0.5 * np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + self.eps))

        return 1 / (1 + distance)
