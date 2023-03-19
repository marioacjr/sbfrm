### Create and activate virtual envirovment for projec ###
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

pip install -r requirements.txt

### Test project
python -m pytest

FILE="../pyinstaller-5.8.0.zip"
if [ ! -f "$FILE" ]; then
    echo "$FILE does not exist."
    wget "https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v5.8.0.zip" -O "../pyinstaller-5.8.0.zip"
fi

FILE="../pyinstaller-5.8.0"
if [ ! -d "$FILE" ]; then
    unzip ../pyinstaller-5.8.0.zip -d ../    
fi

cd ../pyinstaller-5.8.0/bootloader/
python ./waf all --target-arch=64bit
cd ../
pip install .

cd ../sbfrm/
