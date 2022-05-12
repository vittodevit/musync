from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# automatically captured required modules for install_requires in requirements.txt and as well as configure
# dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='musync',
    description='Gets your music from Spotify and downloads it from Youtube Music',
    version='1.0.0',
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    python_requires='>=3.8',  # any python greater than 2.7
    entry_points='''
        [console_scripts]
        musync=src.__main__:main
    ''',
    author="vittodevit",
    keyword="music, spotify, playlist, youtube, download",
    long_description=README,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    url='https://github.com/vittodevit/musync',
    # download_url='https://github.com/CITGuru/cver/archive/1.0.0.tar.gz',
    dependency_links=dependency_links,
    author_email='vittorio@mrbackslash.it',
    classifiers=[
        "License :: OSI Approved :: Apache 2.0 License",
        "Programming Language :: Python :: 3.8",
    ]
)
