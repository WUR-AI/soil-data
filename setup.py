from setuptools import setup, find_packages

setup(
    name='soildata',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'shapely',
        'geopandas',
        'numpy',
        'rasterio',
        'requests',
        'tqdm'
    ],
    author='Diego Quintero', # Replace with your name
    author_email='daquinterop@gmail.com', # Replace with your email
    description='A package for handling soil data, from different data sources.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/soildata', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
