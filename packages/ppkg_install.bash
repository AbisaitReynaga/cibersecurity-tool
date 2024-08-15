#!/bin/bash
PATH=$(pwd)
cd ..
python3 -m venv my-venv
source my-venv/bin/activate

pip install -r $PATH/packages/requirements.txt
