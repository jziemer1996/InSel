from setuptools import setup, find_packages
import os
import sys

directory = os.path.abspath(os.path.dirname(__file__))
if sys.version_info >= (3, 0):
    with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    with open(os.path.join(directory, 'README.md')) as f:
        long_description = f.read()

setup(name='InSel',
      packages=find_packages(),
      include_package_data=True,
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      description='A Python module for processing of SLC scenes using the GAMMA remote sensing software',
      classifiers=[
          'License :: FSF Approved :: GPL-3.0 License',
          'Operating System :: POSIX :: Linux,'
          'Programming Language :: Python',
      ],
      install_requires=["GDAL",
                        'rasterio',
                        'fiona',
                        'numpy',
                        'matplotlib',
                        'sentinelsat',
                        'pyroSAR'],
      python_requires='>=3.6.0',
      url='https://github.com/jziemer1996/InSel.git',
      author='Jonas Ziemer', #'Marlin Mueller'  # how to add second author?
      author_email='jonas.ziemer@uni-jena.de',
      license='GPL-3.0',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')
