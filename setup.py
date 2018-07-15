from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
        
setup(name='pyobiee',
      version='0.1',
      description='Package that enables retrieving data from OBIEE using the webservice.',
      author='Halim Gökduman',
      author_email='halim@skewl.net',
      license='MIT',
      packages=['pyobiee'],
      install_requires=['lxml'],
      dependency_links=['bitbucket.org/jurko/suds/get/tip.tar.gz#egg=suds'],
      include_package_data=True,
      zip_safe=False)