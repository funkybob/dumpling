from setuptools import setup, find_packages

setup(
    name='dumpling',
    version='0.0.1',
    description='A simple CMS for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    keywords=['django', 'cms', 'templates'],
    packages = find_packages(),
    zip_safe=False,
    install_requires=[
        'Django >= 1.8',
        'pyScss >= 1.3.4',
    ]
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
