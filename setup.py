import setuptools

import slide_analysis

with open('requirements.txt') as file:
    INSTALL_REQUIRES = [l.strip() for l in file.readlines() if l]

setuptools.setup(name='slide_analysis',
                 version=slide_analysis.__version__,
                 url='https://github.com/Vozf/slide-analysis/',
                 license='???',  # todo: add
                 description='???',  # todo: add
                 packages=setuptools.find_packages(exclude=['doc']),
                 scripts=['slide_analysis/slide_analysis'],  # todo: rename
                 install_requires=INSTALL_REQUIRES,
                 )
