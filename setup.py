from setuptools import setup, find_packages

setup(
    name='pipmag',
    version='0.1',
    author='Avijeet Prasad',
    author_email='prasad.avijeet@gmail.com',
    description="""Pipeline for magnetic field reconstruction based on
      spectro-polarimetric observations of the solar atmosphere.""",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/AvijeetPrasad/pipmag',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4==4.11.2',
        'ipython==8.10.0',
        'ipywidgets==7.7.3',
        'pandas==1.5.3',
        'requests==2.31.0'
    ],
    python_requires='>=3.10',
)
