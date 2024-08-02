import tokener as tk
import sys
import subprocess
from PySide6 import QtWidgets, QtCore

location = "/Users/ieatsoulsmeow/Desktop/Python Lessons/picopy/example.pcpy"

with open(location, "r") as file:
    lines = file.readlines()
print(lines)

#This is for creating a reading variables!
variables = {}

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.text_box = QtWidgets.QPlainTextEdit(self)
        self.text_box.insertPlainText("Running " + location)
        self.text_box.resize(800,600)
        self.text_box.setReadOnly(True)
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.run_after_open)
        self.timer.start(100)  # Run the method after 100 milliseconds

    @QtCore.Slot()
    def run_after_open(self):
        skip_line = -1
        for i in range(len(lines)):
            if tk.count_leading_tabs(lines[i]) >= skip_line:
                skip_line = -1
                tokenised = tk.tokenise_save(lines[i])
                print(tokenised)
                if tokenised[0].lower() == "send":
                    if tk.is_string(tokenised[2]):
                        self.text_box.appendPlainText(tk.grab_between(lines[i], '"', 0))
                    elif tokenised[2] in variables:
                        self.text_box.appendPlainText(variables[tokenised[2]])
                    else:
                        self.text_box.appendPlainText("Error: Couldn't sparse '" + lines[i].rstrip('\n') + "' with error in " + tokenised[2])
                elif tokenised[0].lower() == "var":
                        if tk.is_string(tk.seperate_spaces(lines[i])[3]):
                            variables[tokenised[1]] = tk.grab_between(lines[i], '"', 0)
                            print(tk.grab_between(lines[i], '"', 0))
                        else:
                            self.text_box.appendPlainText("Error: Couldn't sparse '" + lines[i].rstrip('\n') + "' with error in " + tokenised[3])
                elif tokenised[0].lower() == "if":
                    if tokenised[1].lower() == "false":
                        skip_line = tk.count_leading_tabs(lines[i]) + 1
                    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setMinimumSize(800, 600)
    widget.show()

    sys.exit(app.exec())