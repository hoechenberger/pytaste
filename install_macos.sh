#!/usr/bin/env bash

conda env create -n pytaste -f pytaste/conda/environment_macos.yml
source activate pytaste
pip install --no-deps psychopy==1.90.1
source deactivate
