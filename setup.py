from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
        
setup(name='pyobiee',
      version='0.14',
      description='Package that enables retrieving data from OBIEE using the webservice.',
      author='Halim Gökduman',
      author_email='halim@skewl.net',
      license='MIT',
      packages=['pyobiee'],
      install_requires=['lxml', 'suds-community'],
      include_package_data=True,
      zip_safe=False,
	  url='https://github.com/hgokduman/pyobiee')
