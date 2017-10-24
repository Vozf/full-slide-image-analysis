from functools import reduce
from slide_analysis.descriptors import all_descriptors

def _compose_util(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(_compose_util, fs)


def get_descriptor_class_by_name(name):
    return next((x for x in all_descriptors if x.__name__ == name), None)
