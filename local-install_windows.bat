python.exe -m venv .venv

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt

.venv\Scripts\python.exe -m pytest
