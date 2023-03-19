pyinstaller --clean --noconsole --onefile sbfrm_gui.py;
pyinstaller --clean --noconsole --onefile sbfrm.py;
mv dist/sbfrm_gui releases/linux/sbfrm-gui;
mv dist/sbfrm releases/linux/sbfrm;
