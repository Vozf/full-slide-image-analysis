import setuptools

import full_slide_image_analysis

with open('requirements.txt') as file:
    INSTALL_REQUIRES = [l.strip() for l in file.readlines() if l]

setuptools.setup(name='full_slide_image_analysis',
                 version=full_slide_image_analysis.__version__,
                 url='https://github.com/Vozf/full-slide-image-analysis/',
                 license='???',  # todo: add
                 description='???',  # todo: add
                 packages=setuptools.find_packages(exclude=['doc']),
                 scripts=['full_slide_image_analysis/full_slide_image_analysis'],  # todo: rename
                 install_requires=INSTALL_REQUIRES,
                 )
