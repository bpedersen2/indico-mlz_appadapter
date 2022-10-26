'''
Created on Mar 9, 2018

@author: pedersen
'''
from __future__ import unicode_literals

from setuptools import find_packages, setup

setup(
    name='indico-mlz-appadapter',
    url='https://github.com/bpedersen2/mlz-indico-appadapter',
    license='MIT',
    author='MLZ Indico Team',
    author_email='bjoern.pedersen@frm2.tum.de',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    use_scm_version={"write_to":"indico_mlz_appadapter/version.py",
                     "local_scheme":"node-and-timestamp"},
    setup_requires = ["setuptools>=39", "setuptools_scm[toml]>=3.4"],
    install_requires=['indico>=2.3.0'],
    entry_points={
        'indico.plugins': {'mlz_appadapter = indico_mlz_appadapter.plugin:MLZAppAdapterPlugin'},
    },
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
