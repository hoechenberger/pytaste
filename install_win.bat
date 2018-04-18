conda env create -n pytaste -f pytaste\conda\environment_win.yml
activate pytaste
pip install --no-deps psychopy==1.90.1
deactivate
