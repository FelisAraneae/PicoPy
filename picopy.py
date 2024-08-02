import tokener as tk
import sys
import subprocess
import os
import shutil
from PySide6 import QtCore, QtWidgets, QtGui

file_path = '/Users/ieatsoulsmeow/Desktop/Python Lessons/picopy/example.pcpy'
backup_dir = '/Users/ieatsoulsmeow/Desktop/Python Lessons/picopy/backup/'

with open(file_path, 'r') as file:
    lines = file.readlines()
print(lines)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.text_box = QtWidgets.QPlainTextEdit(self)
        self.text_box.insertPlainText(tk.listToString(lines))
        self.text_box.resize(800,550)

        self.save = QtWidgets.QPushButton(self)
        self.save.setText("Save")
        self.save.move(100,550)
        self.save.resize(100,48)
        self.save.clicked.connect(self.save_code)

        self.run = QtWidgets.QPushButton(self)
        self.run.setText("Run")
        self.run.move(600,550)
        self.run.resize(100,48)
        self.run.clicked.connect(self.run_file)

        self.undo = QtWidgets.QPushButton(self)
        self.undo.setText("Undo")
        self.undo.move(350,550)
        self.undo.resize(100,48)
        self.undo.clicked.connect(self.revert_to_last_file)

    def save_code(self):
        with open(file_path, 'r') as file:
            current_content = file.read()

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        existing_backups = [f for f in os.listdir(backup_dir) if f.startswith('example_backup_') and f.endswith('.pcpy')]
        existing_backups.sort()

        if existing_backups:
            latest_backup_file = existing_backups[-1]
            latest_backup_number = int(latest_backup_file.split('_')[-1].split('.')[0])
            next_backup_number = latest_backup_number + 1

            latest_backup_path = os.path.join(backup_dir, latest_backup_file)
            with open(latest_backup_path, 'r') as latest_file:
                latest_content = latest_file.read()

            if current_content == latest_content:
                print("The content is the same as the latest backup. No new backup created.")
            else:
                backup_file_path = os.path.join(backup_dir, f'example_backup_{next_backup_number}.pcpy')
                with open(backup_file_path, 'w') as backup_file:
                    backup_file.write(current_content)
                print(f"File backed up to {backup_file_path}")
        else:
            next_backup_number = 0
            backup_file_path = os.path.join(backup_dir, f'example_backup_{next_backup_number}.pcpy')
            with open(backup_file_path, 'w') as backup_file:
                backup_file.write(current_content)
            print(f"File backed up to {backup_file_path}")

        content = self.text_box.toPlainText()
        with open(file_path, 'w') as file:
            file.write(content)

    @QtCore.Slot()
    def run_file(self):
        subprocess.Popen(["python", "/Users/ieatsoulsmeow/Desktop/Python Lessons/picopy/picopy_run.py"])

    @QtCore.Slot()
    #ChatGPT
    def revert_to_last_file(self):
        # Get list of existing backup files
        existing_backups = [f for f in os.listdir(backup_dir) if f.startswith('example_backup_') and f.endswith('.pcpy')]
        existing_backups.sort()

        if existing_backups:
            # Get the latest backup file
            latest_backup_file = existing_backups[-1]
            latest_backup_path = os.path.join(backup_dir, latest_backup_file)

            # Copy the content from the latest backup file to the original file
            with open(latest_backup_path, 'r') as backup_file:
                backup_content = backup_file.read()

            with open(file_path, 'w') as original_file:
                original_file.write(backup_content)

            # Delete the latest backup file
            os.remove(latest_backup_path)
            print(f"Reverted to the file from backup: {latest_backup_file}")
            self.text_box.setPlainText(tk.listToString(backup_content))
        else:
            print("No backup files available to revert.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.setMinimumSize(800, 600)
    widget.show()

    sys.exit(app.exec())