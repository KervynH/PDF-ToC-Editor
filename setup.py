from setuptools import setup


setup(
    name = 'pdf-toc-cli',
    version = '0.1.0',
    packages = ['src'],
    entry_points = {
        'console_scripts': [
            'toc = src.__main__: main'
        ]
    }
)
