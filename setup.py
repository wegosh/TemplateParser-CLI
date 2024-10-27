from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='template_parser',
    version='1.0.0',
    description='A CLI tool for parsing templates and replacing placeholders in a JSON file.',
    author='Patryk Wegrzynski',
    author_email='wegosh16@gmail.com',
    url='https://github.com/wegosh/JSON-template-parser',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'template-parser=template_parser.main:main',
        ],
    },
    include_package_data=True,
)
