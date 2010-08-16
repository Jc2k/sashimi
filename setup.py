from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'sashimi',
    version = version,
    description = "A Plone fuzzing library",
    long_description = open("README.rst").read() + "\n" + open("CHANGES.txt").read(),
    classifiers = [
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords = "plone fuzzing",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
    },
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
    ],
    extras_require = {
        "test": [
            "Mock",
            "coverage",
            "uuid",
            # Dependencies for Zope/Plone testing
            "Zope2 == 2.12.8",
            "Products.Archetypes",
            ],
    },
)

