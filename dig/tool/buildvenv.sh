#!/bin/sh

oldcwd = `pwd`
cd /opt/dig/project/dig-extract
python setup.py install
cd /opt/dig/venv/dig
zip -r /opt/dig/venv/digvenv.zip *
cd $oldcwd
