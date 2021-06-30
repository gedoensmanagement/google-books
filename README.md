# google-books
A Python script to download color images of public domain books on Google Books.

(Does not work with copyrighted books! Tested with Python 3.8 on Windows and Linux.)

## Installation
* Create a new environment with Python 3.8 using [venv](https://docs.python-guide.org/dev/virtualenvs/) or [conda](https://docs.anaconda.com/), e.g. `conda create --name dh_blog python=3.8`.
* Activate the new environment, e.g. `conda activate dh_blog`.
* Use pip to install the `requirements.txt`: `pip install -r requirements.txt`.
* Download one of the selenium drivers listed in https://selenium-python.readthedocs.io/installation.html#drivers. (The script is pre-configured for Edge on Windows and Gecko on Linux. Modify lines 75ff in `books.py` if you use other combinations!)
* Create a subfolder with a name corresponding to the chosen driver (i.e. "geckodriver", "edgedriver", "chromedriver"). (Modify lines 75ff in `books.py` if necessary!)
* Unpack the downloaded `zip`-file to this subfolder.

## Usage
* Run the script with `python books.py` to download 10 pages of a pre-configured book.
* Read the instructions in `books.py` and modify the variables to fit your requirements.
