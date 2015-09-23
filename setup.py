from distutils.core import setup

setup(name = "pyhurdy",
    version = "0.1",
    package_dir={'': 'pyhurdy'},
    py_modules=['pyhurdy'],
    description = "Python Hurdy Gurdy Project",
    author = "elizabeth.flanagan@intel.com",
    author_email = "Beth Flanagan",
    url = "https://github.com/yoctopidge/pyhurdy",
    license = "GPL-3.0",
    package_data = {'': ['pyhsounds/*/*.wav']},

#    data_files = [('/usr/lib', ["pygurdysounds"])]
)

