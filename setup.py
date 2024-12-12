from setuptools import setup, find_packages

'''
python3 -m unittest
vim setup.py
rm -rf dist/
python3 setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
'''

def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(name="othelloAI-canvas",
      version="0.1.0",
      license='Apache',
      description="A Python library for Othello AI with AI vs AI functionality",
      url="https://github.com/Wawawa2525/othelloAI-canvas",
      packages=['othelloAI_canvas'],
      # package_dir={"": "src"},
      package_data={'othelloAI_canvas': ['./*.*']},
      install_requires=_requires_from_file('requirements.txt'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: Apache Software License',
          'Framework :: IPython',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Intended Audience :: Education',
      ],
      )
