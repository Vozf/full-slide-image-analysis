from slide_analysis.descriptors import HistogramDescriptor
from slide_analysis.descriptors import TestDescriptor
from slide_analysis.initialize_base_service import InitBaseService
from slide_analysis.splitting_service import SplittingService

class Model:
    def __init__(self):
        self.descriptors = [HistogramDescriptor, TestDescriptor]

    def calculate_descriptors(self, idx, filepath, directory_path):
        split = SplittingService()
        stream = split.split_to_tiles(filepath)

        init_base = InitBaseService(directory_path)
        init_base.init_base(stream, HistogramDescriptor, (2, 2, 3), 'image', 'class')
