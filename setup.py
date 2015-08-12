from setuptools import setup
setup(
  name='quiver',
  packages=['quiver'],
  version='0.1',
  description='A simple library to plot direction fields',
  author='Casey Davidson',
  author_email='jdavids2@gmail.com',
  url='https://github.com/davidsoncasey/quiver',
  download_url='https://github.com/davidsoncasey/quiver/tarball/0.1',
  keywords=['plotting', 'direction field', 'differential equation'],
  classifiers=[],
  license='MIT',
  install_requires=[
    'matplotlib',
    'numpy',
    'sympy',
  ],
)