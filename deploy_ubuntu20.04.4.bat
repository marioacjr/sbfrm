python.exe -m venv .env

.env\Scripts\pip.exe install --upgrade pip
.env\Scripts\pip.exe install -r requirements.txt

.env\Scripts\python.exe -m pytest
