import setuptools

with open("README.md", "r") as f:
  long_description = f.read()

setuptools.setup(
  name="hsbc_csv_parse",
  version="0.01",
  author="Christopher Simpson",
  author_email="chris15leicester@gmail.com",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url=None,
  packages=setuptools.find_packages(),
  data_files=None,
  include_package_data=False,
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3",
  install_requires=[]
  
)
