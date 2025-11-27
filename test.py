import sys
import json
from pathlib import Path
from moviepy import VideoFileClip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QFileDialog, QDialog, 
                             QLineEdit, QCheckBox, QComboBox, QSpinBox, QGroupBox)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle('// Settings')
        self.setGeometry(200, 200, 500, 400)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Folders group
        folders_group = QGroupBox("// Folders")
        folders_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        folders_layout = QVBoxLayout()
        
        # Videos folder
        videos_layout = QHBoxLayout()
        self.videos_path_edit = QLineEdit(str(self.parent_window.videos_folder))
        self.videos_path_edit.setStyleSheet(self._get_input_style())
        videos_browse_btn = QPushButton('Browse')
        videos_browse_btn.setStyleSheet(self._get_small_btn_style())
        videos_browse_btn.clicked.connect(lambda: self.browse_folder('videos'))
        videos_layout.addWidget(QLabel('Videos folder:'))
        videos_layout.addWidget(self.videos_path_edit)
        videos_layout.addWidget(videos_browse_btn)
        
        # Sounds folder
        sounds_layout = QHBoxLayout()
        self.sounds_path_edit = QLineEdit(str(self.parent_window.sounds_folder))
        self.sounds_path_edit.setStyleSheet(self._get_input_style())
        sounds_browse_btn = QPushButton('Browse')
        sounds_browse_btn.setStyleSheet(self._get_small_btn_style())
        sounds_browse_btn.clicked.connect(lambda: self.browse_folder('sounds'))
        sounds_layout.addWidget(QLabel('Sounds folder:'))
        sounds_layout.addWidget(self.sounds_path_edit)
        sounds_layout.addWidget(sounds_browse_btn)
        
        folders_layout.addLayout(videos_layout)
        folders_layout.addLayout(sounds_layout)
        folders_group.setLayout(folders_layout)
        
        # Audio quality group
        quality_group = QGroupBox("Quality")
        quality_group.setStyleSheet(folders_group.styleSheet())
        quality_layout = QVBoxLayout()
        
        bitrate_layout = QHBoxLayout()
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(['128k', '192k', '256k', '320k'])
        self.bitrate_combo.setCurrentText(self.parent_window.settings.get('bitrate', '192k'))
        self.bitrate_combo.setStyleSheet(self._get_input_style())
        bitrate_layout.addWidget(QLabel('Bitrate:'))
        bitrate_layout.addWidget(self.bitrate_combo)
        bitrate_layout.addStretch()
        
        quality_layout.addLayout(bitrate_layout)
        quality_group.setLayout(quality_layout)
        
        # General settings group
        general_group = QGroupBox("General")
        general_group.setStyleSheet(folders_group.styleSheet())
        general_layout = QVBoxLayout()
        
        self.delete_after_check = QCheckBox('Delete original MP4 after conversion')
        self.delete_after_check.setChecked(self.parent_window.settings.get('delete_after', False))
        self.delete_after_check.setStyleSheet("color: #ff6b6b;")
        
        self.open_folder_check = QCheckBox('Open output folder after conversion')
        self.open_folder_check.setChecked(self.parent_window.settings.get('open_folder', False))
        self.open_folder_check.setStyleSheet("color: #ffffff;")
        
        general_layout.addWidget(self.delete_after_check)
        general_layout.addWidget(self.open_folder_check)
        general_group.setLayout(general_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        # Add all to main layout
        layout.addWidget(folders_group)
        layout.addWidget(quality_group)
        layout.addWidget(general_group)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def _get_input_style(self):
        return """
            QLineEdit, QComboBox {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """
    
    def _get_small_btn_style(self):
        return """
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """
    
    def browse_folder(self, folder_type):
        folder = QFileDialog.getExistingDirectory(self, f"Select {folder_type.capitalize()} Folder")
        if folder:
            if folder_type == 'videos':
                self.videos_path_edit.setText(folder)
            else:
                self.sounds_path_edit.setText(folder)
    
    def save_settings(self):
        self.parent_window.videos_folder = Path(self.videos_path_edit.text())
        self.parent_window.sounds_folder = Path(self.sounds_path_edit.text())
        
        # Create folders if they don't exist
        self.parent_window.videos_folder.mkdir(exist_ok=True)
        self.parent_window.sounds_folder.mkdir(exist_ok=True)
        
        # Save settings to dict
        self.parent_window.settings = {
            'videos_folder': str(self.parent_window.videos_folder),
            'sounds_folder': str(self.parent_window.sounds_folder),
            'bitrate': self.bitrate_combo.currentText(),
            'delete_after': self.delete_after_check.isChecked(),
            'open_folder': self.open_folder_check.isChecked()
        }
        
        # Save to file
        self.parent_window.save_settings()
        self.parent_window.log("// ✓ settings saved!")
        self.accept()


class ConverterThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, files, output_folder, settings):
        super().__init__()
        self.files = files
        self.output_folder = output_folder
        self.settings = settings
    
    def run(self):
        if not self.files:
            self.log_signal.emit("// no files selected ( ͡° ͜ʖ ͡°)")
            self.finished_signal.emit()
            return
        
        self.log_signal.emit(f"// converting {len(self.files)} file(s)...")
        
        for mp4_file in self.files:
            try:
                self.log_signal.emit(f"// converting, pls wait >_<: {mp4_file.name}")
                video = VideoFileClip(str(mp4_file))
                output_path = self.output_folder / f"{mp4_file.stem}.mp3"
                
                # Get bitrate from settings
                bitrate = self.settings.get('bitrate', '192k')
                video.audio.write_audiofile(str(output_path), bitrate=bitrate, logger=None)
                video.close()
                
                self.log_signal.emit(f"// ✓ converted: {output_path.name}")
                
                # Delete original if setting enabled
                if self.settings.get('delete_after', False):
                    mp4_file.unlink()
                    self.log_signal.emit(f"// 🗑 deleted: {mp4_file.name}")
                    
            except Exception as e:
                self.log_signal.emit(f"// ✗ error converting {mp4_file.name}: {str(e)}")
        
        self.log_signal.emit("\n// conversion completed! enjoy! ƪ(˘⌣˘)ʃ")
        self.finished_signal.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_dir = Path(__file__).parent
        self.settings_file = self.script_dir / "converter_settings.json"
        
        # Load settings
        self.load_settings()
        
        # Setup paths from settings
        self.videos_folder = Path(self.settings.get('videos_folder', str(self.script_dir / "videos")))
        self.sounds_folder = Path(self.settings.get('sounds_folder', str(self.script_dir / "sounds")))
        
        # Create folders
        self.sounds_folder.mkdir(exist_ok=True)
        self.videos_folder.mkdir(exist_ok=True)
        
        self.selected_files = []
        self.converter_thread = None
        self.init_ui()
    
    def load_settings(self):
        """Load settings from JSON file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            except:
                self.settings = self.get_default_settings()
        else:
            self.settings = self.get_default_settings()
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get_default_settings(self):
        """Return default settings"""
        return {
            'videos_folder': str(self.script_dir / "videos"),
            'sounds_folder': str(self.script_dir / "sounds"),
            'bitrate': '192k',
            'delete_after': False,
            'open_folder': False
        }
    
    def init_ui(self):
        self.setWindowTitle('MP4 → MP3 Converter ♪(´ε` )')
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #2b2b2b;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title and settings button layout
        title_layout = QHBoxLayout()
        title = QLabel('MP4 → MP3 Converter ♪(´ε` )')
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; padding: 10px;")
        
        settings_btn = QPushButton('⚙')
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 18px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(settings_btn)
        
        # Select files button
        self.select_btn = QPushButton('Select MP4 Files')
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.select_btn.clicked.connect(self.select_files)
        
        # Files label
        self.files_label = QLabel('// no files selected')
        self.files_label.setStyleSheet("color: #ffaa00; font-size: 14px;")
        
        # Convert button
        self.convert_btn = QPushButton('Convert')
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
        """)
        self.convert_btn.clicked.connect(self.start_conversion)
        
        # Log text area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #555;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }
        """)
        self.log_area.setText('// logs will appear here...\n')
        
        # Add widgets to layout
        layout.addLayout(title_layout)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.files_label)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.log_area)
        
        central_widget.setLayout(layout)
    
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select MP4 Files",
            str(self.videos_folder),
            "MP4 Files (*.mp4);;All Files (*)"
        )
        
        if files:
            self.selected_files = [Path(f) for f in files]
            self.files_label.setText(f'// selected {len(self.selected_files)} file(s) ✓')
            self.log(f"// selected: {', '.join([f.name for f in self.selected_files])}")
    
    def start_conversion(self):
        if self.converter_thread and self.converter_thread.isRunning():
            self.log("// conversion already in progress...")
            return
        
        if not self.selected_files:
            self.selected_files = list(self.videos_folder.glob("*.mp4"))
            if not self.selected_files:
                self.log("// no mp4 files found in videos folder...")
                self.log("// maybe next time ( ͡° ͜ʖ ͡°)")
                return
        
        self.convert_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        
        self.converter_thread = ConverterThread(self.selected_files, self.sounds_folder, self.settings)
        self.converter_thread.log_signal.connect(self.log)
        self.converter_thread.finished_signal.connect(self.conversion_finished)
        self.converter_thread.start()
    
    def conversion_finished(self):
        self.convert_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        self.selected_files = []
        self.files_label.setText('// no files selected')
        
        # Open folder if setting enabled
        if self.settings.get('open_folder', False):
            import os
            os.startfile(self.sounds_folder)
    
    def log(self, message):
        self.log_area.append(message)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
