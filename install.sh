#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh
sudo apt-get install -y \
  python-dev \
  python-pip \
  python-numpy \
  python-scipy \
  cython \

sudo pip install virtualenv
sudo pip install virtualenvwrapper
mkvirtualenv venv
workon venv
pip install -r requirements.txt
pip install pytest
pip uninstall -y pydot
git clone https://github.com/joschu/cgt ~/code/cgt
add2virtualenv ~/code/cgt
