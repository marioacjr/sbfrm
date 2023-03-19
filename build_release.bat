.venv_win\Scripts\pyinstaller.exe --clean --noconsole --onefile sbfrm_gui.py
.venv_win\Scripts\pyinstaller.exe --clean --noconsole --onefile sbfrm.py
move .\dist\sbfrm.exe .\releases\windows\
move .\dist\sbfrm_gui.exe .\releases\windows\