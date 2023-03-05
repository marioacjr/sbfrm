# sudo apt install python3-tk

### Create and activate virtual envirovment for projec ###
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

pip install -r requirements.txt

# ### Install pyTest and test project
# sudo apt install python3-pytest
python -m pytest
