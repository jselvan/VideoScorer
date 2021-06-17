from setuptools import setup, find_packages

setup(
    name="VideoScorer",
    packages=find_packages(),
    author='Janahan Selvanayagam',
    author_email='seljanahan@hotmail.com',
    install_requires=[
        'numpy',
        'pandas',
        'python-vlc',
        'click'
    ],
    entry_points='''
        [console_scripts]
        VideoScorer=VideoScorer.__main__:main
    ''',
    zip_safe=False
)