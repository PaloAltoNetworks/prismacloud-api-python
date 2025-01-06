import importlib
import os
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

spec = importlib.util.spec_from_file_location(
    'prismacloud.api.version', os.path.join('prismacloud', 'api', 'version.py')
)

mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
version = mod.version

setuptools.setup(
    name='prismacloud-api',
    version=version,
    author='Tom Kishel',
    author_email='tkishel@paloaltonetworks.com',
    description='Prisma Cloud API SDK for Python',
    keywords="prisma cloud api",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PaloAltoNetworks/prismacloud-api-python',
    packages=setuptools.find_namespace_packages(exclude=['scripts']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    install_requires=[
        'requests',
        'update_checker'
    ],
    extras_require={
        'test': ['coverage==7.6.10', 'responses==0.25.3']
    },
    python_requires='>=3.6'
)
