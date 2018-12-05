from setuptools import setup

setup(name='tak-tent',
      version='0.9',
      description='A framework for conducting agent-based simulations of SETI',
      url='http://github.com/dh4gan/tak-tent',
      author='Duncan Forgan',
      author_email='dh4gan@gmail.com',
      license='GPL-3.0',
      install_requires=['numpy','matplotlib']
      packages=find_packages(exclude=['tests*']),
      zip_safe=False)
