## to exe command

pyinstaller --onefile --icon=icon.ico main.py

pyinstaller --onefile --noconsole --icon=icon.ico --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets test.py
