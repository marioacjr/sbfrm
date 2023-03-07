.venv\Scripts\pyinstaller.exe --noconsole --onefile sbfrm_gui.py
.venv\Scripts\pyinstaller.exe --noconsole --onefile sbfrm.py
move .\dist\sbfrm.exe .\releases\windows\
move .\dist\sbfrm_gui.exe .\releases\windows\