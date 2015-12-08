#!/bin/bash
# This script is not needed on Raspbian Jessie installations
sudo apt-get install -y python3-setuptools python3-pip
sudo pip-3.2 install pgzero

# Remove the line that fails with this version of pygame/python3
sudo patch /usr/local/lib/python3.2/dist-packages/pgzero/rect.py wheezy-patch/rect.py.patch
