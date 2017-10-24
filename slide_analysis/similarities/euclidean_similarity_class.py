import numpy as np


class EuclideanSimilarity:
    @staticmethod
    def compare(hist1, hist2):
        return 1 / (1 + np.linalg.norm(hist1 - hist2))


if __name__ == '__main__':
    print(EuclideanSimilarity.compare(np.array([1, 2, 3]), np.array([2, 2, 3])))
    print(EuclideanSimilarity.compare(np.array([1, 2, 3]), np.array([2, 3, 4])))
    print(EuclideanSimilarity.compare(np.array([1, 2, 3]), np.array([1, 2, 3])))
