# last change

import sys
import os

import time
import threading
from chatbot import ChatBotUI
from ConversationManager import  get_call_summary

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QFileDialog,
    QMessageBox,
)
import whisper
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QDateTime
import torchaudio
from buzz.widgets.audio_player import AudioPlayer
from buzz.widgets.icon import UndoIcon






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 500)
        self.setWindowTitle("Audio File Manager")

        # Dictionary to store transcriptions
        self.transcriptions = {}

        # Initialize the table
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.table.setRowCount(0)
        self.table.setColumnCount(5)  # Added 'Time Added' column
        self.table.setHorizontalHeaderLabels(["File Name", "Status", "Date Added", "Time Added", "Model"])
        self.table.setStyleSheet("QTableWidget::item { padding: 10px; }")

        # Create toolbar
        self.create_toolbar()
        
        self.language_selector = LanguageSelectionDialog()

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        

        # Create a QWidget to hold the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load previously saved audio file (optional feature)
        self.load_previous_audio()
        
    def transcribe(self, audio_path, language, locally = False):
        global transcription_data
        print(f"transcribing in {language}")

        if locally:
            print("processing transcriptions locally")
            print(f"processing transciptions for  file at {audio_path}")
            result = transcribe_audio(file_path = audio_path, language = language)
            segments = extract_segments(result['segments'])
        
            
        else:
            result = request_transcription(file_path = audio_path, language = language)
            segments = extract_and_align_segments(result, language)
                   
        results = segments
            
        
        print("results of transciptions:", results)
        file_name = os.path.basename(audio_path)
        transcription_data[file_name] = results
        self.update_status_by_filename(file_name= file_name, new_status = "Complete")
        
    def get_segments(self, audio_path, language):
        print(f"processing transciptions for  file at {audio_path}")
        transcription_thread = threading.Thread(target = self.transcribe, args= [audio_path, language])
        transcription_thread.start() 

    def create_toolbar(self):
        """Creates the toolbar with Add, Delete, and View Transcription buttons."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Add File Button (+ icon)
        add_file_action = QAction(QIcon.fromTheme("list-add"), "Add File", self)
        add_file_action.triggered.connect(self.add_file)
        toolbar.addAction(add_file_action)

        # Delete File Button (🗑️ icon)
        delete_file_action = QAction(QIcon.fromTheme("edit-delete"), "Delete File", self)
        delete_file_action.triggered.connect(self.delete_file)
        toolbar.addAction(delete_file_action)

        # View Transcription Button (expand icon)
        view_transcription_action = QAction(QIcon.fromTheme("document-preview"), "View Transcription", self)
        view_transcription_action.triggered.connect(self.view_transcription)
        toolbar.addAction(view_transcription_action)

    def add_file(self):
        """Allows the user to add an audio file to the list."""
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an Audio File",
            "",
            "Audio Files (*.flac *.wav);;All Files (*)",
            options=options
        )

        if file_path:
            if self.language_selector.exec():  # This should happen on the main thread
                selected_language = self.language_selector.get_selected_language()
                print(f"Selected language: {selected_language}")
                
            self.get_segments(audio_path= file_path, language = selected_language)
            file_name = os.path.basename(file_path)
            current_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
            status = "Pending"
            model = "N/A"
            
            self.add_entry_to_table(file_name = file_name,
                                    file_path  = file_path,
                                    current_date = current_date,
                                    current_time = current_time,
                                    status = status,
                                    model =  model
                                    )
            self.add_entry_to_tranacription_db(file_name = file_name,
                                    file_path = file_path,
                                    current_date = current_date,
                                    current_time = current_time,
                                    status = status,
                                    model =  model
                                    )
            
            # Initialize empty transcription
            self.transcriptions[file_name] = None  

    def delete_file(self, update_db = True):
        """Deletes the selected file from the table."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            file_name = self.table.item(selected_row, 0).text() # Get filename
            self.table.removeRow(selected_row)
            self.remove_entry_from_transcription_db(filename = file_name )
            if update_db:
                self.remove_entry_from_transcription_db(filename = file_name)
            
            # Remove transcription if it exists
            if file_name in self.transcriptions:
                del self.transcriptions[file_name]
        else:
            QMessageBox.warning(self, "Delete File", "Please select a file to delete.")
            
    def add_entry_to_tranacription_db(self, file_name, file_path, status, current_date, current_time, model):
        entry = {"file_name"    : file_name,
                "file_path"     : file_path,
                "current_date"  : current_date,
                "current_time"  : current_time,
                "status"        : status,
                "model"         : model}
        transcriptions.append(entry)
        print("added to the transcription db")
        print(f"db now contains {transcriptions}")
        
    def remove_entry_from_transcription_db(self, filename):
        global transcriptions
        transcriptions =  [entry for entry in transcriptions if entry["file_name"] != filename]
        print(f"updates trancriptions {transcriptions}")  
        
    def add_entry_to_table(self, file_name, file_path, status, current_date, current_time, model, update_db =True):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(file_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(status))
        self.table.setItem(row_position, 2, QTableWidgetItem(current_date))
        self.table.setItem(row_position, 3, QTableWidgetItem(current_time))
        self.table.setItem(row_position, 4, QTableWidgetItem(model))
        
        if update_db:
            self.add_entry_to_tranacription_db(file_name = file_name,
                                    file_path = file_path,         
                                    current_date = current_date,
                                    current_time = current_time,
                                    status = status,
                                    model =  model
                                    )

    def update_status_by_filename(self, file_name, new_status):
        # Iterate through rows to find the matching file name
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)  # Column 0 contains file_name
            if item and item.text() == file_name:
                self.table.setItem(row, 1, QTableWidgetItem(new_status))  # Column 1 is status
                print(f"Updated status of '{file_name}' to '{new_status}'")
                return  # Exit after updating the first match

        print(f"File '{file_name}' not found in table.")       

    def load_previous_audio(self):
        
        file_name = "sample2.flac"
        file_path = "C:/Users/sudar/Downloads/sample2.flac"
        current_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
        status = "Complete"
        model = "N/A"
        
        self.add_entry_to_table(file_name = file_name,
                                file_path = file_path,
                                current_date = current_date,
                                current_time = current_time,
                                status = status,
                                model =  model)
        
        transcription_data[file_name] = sample_transcriptions
        print(transcription_data)

    def view_transcription(self):
        """Displays the transcription of the selected file if the status is 'Complete'."""
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            file_name = self.table.item(selected_row, 0).text()
            status = self.table.item(selected_row, 1).text()

            if status == "Complete":
                transcription = self.transcriptions.get(file_name, "No transcription available.")
                self.transcription_window = TranscriptionWindow(file_name)
                self.transcription_window.show()
                
            else:
                QMessageBox.warning(self, "View Transcription", "Transcription is only available for completed files.")
        else:
            QMessageBox.warning(self, "View Transcription", "Please select a file to view the transcription.")
