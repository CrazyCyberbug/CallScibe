
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QComboBox,
    QFileDialog,
    QSplitter,
    QScrollArea,
    QLabel,
    QMenu,
    QPushButton,
    QHBoxLayout,
    
)
import whisper
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QRect
import torchaudio
from buzz.widgets.audio_player import AudioPlayer
from buzz.widgets.icon import UndoIcon






class TranscriptionWindow(QMainWindow):
    def __init__(self, file_name):
        super().__init__()
        file_path = get_file_path(file_name)
        file_name = os.path.basename(file_path)
        self.file_name = file_name
        self.file_path = file_path
        self.segments = transcription_data[file_name]
        self.transcript = consolidate_transcripts(self.segments)
        self.setGeometry(0, 0, 1200, 700)
        self.setWindowTitle(f"{file_name} - Transcription viewer")

        # Main Splitter (Side panel + Main content)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.main_splitter)

        # Sidebar (Persistent)
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)

        # Buttons for toggling panels with icons
        self.summary_button = QPushButton()
        self.summary_button.setIcon(QIcon("icons/summaryIcon.png"))
        self.summary_button.setIconSize(QRect(0, 0, 20, 20).size())
        self.summary_button.setFixedSize(35, 35)
        self.summary_button.clicked.connect(self.toggle_summary_panel)

        self.chatbot_button = QPushButton()
        self.chatbot_button.setIcon(QIcon("icons/chatIcon.png"))
        self.chatbot_button.setIconSize(QRect(0, 0, 20, 20).size())
        self.chatbot_button.setFixedSize(35, 35)
        self.chatbot_button.clicked.connect(self.open_chatbot_window)

        sidebar_layout.addWidget(self.summary_button)
        sidebar_layout.addWidget(self.chatbot_button)
        sidebar_layout.addStretch()
        sidebar_layout.setSpacing(15)
        self.sidebar.setLayout(sidebar_layout)
        self.sidebar.setFixedWidth(45)

        # Summary Panel (Collapsible)
        self.summary_panel = QWidget()
        summary_layout = QVBoxLayout(self.summary_panel)
        summary_label = QLabel("Summary", self)
        summary_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        summary = get_call_summary(self.transcript)
        self.summary_text = QLabel(summary, self)
        self.summary_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.summary_text.setWordWrap(True)
        summary_text_scroll = QScrollArea()
        summary_text_scroll.setWidget(self.summary_text)
        summary_text_scroll.setWidgetResizable(True)
        summary_layout.addWidget(summary_label)
        summary_layout.addWidget(summary_text_scroll)
        self.summary_panel.setLayout(summary_layout)

        # Main content widget
        self.main_content = QWidget()
        self.layout = QVBoxLayout(self.main_content)

        # Add toolbar
        self.create_toolbar()

        # Add display options
        self.setup_display_options()

        # Set up table view with initial settings
        self.setup_table()

        # Set up the audio player
        ppath = file_path
        self.audio_player = AudioPlayer(file_path=ppath)
        self.audio_player.position_ms_changed.connect(self.on_audio_player_position_ms_changed)

        # Create a horizontal layout for the audio player and reset button
        audio_controls_layout = QHBoxLayout()

        # Add Reset Playback button
        self.reset_button = QPushButton(self)
        self.reset_button.setIcon(UndoIcon(self))
        self.reset_button.setToolTip("Reset Playback")
        self.reset_button.setFixedSize(30, 30)
        self.reset_button.clicked.connect(self.reset_playback)
        audio_controls_layout.addWidget(self.reset_button)

        # Add the audio player next to the reset button
        audio_controls_layout.addWidget(self.audio_player)
        self.layout.addLayout(audio_controls_layout)

        # Set up subtitle label
        self.subtitle_label = QLabel("", self)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("font-size: 16px; color: white; padding: 10px;")
        self.layout.addWidget(self.subtitle_label)

        # Add widgets to splitter
        self.main_splitter.addWidget(self.sidebar)
        self.main_splitter.addWidget(self.summary_panel)
        self.main_splitter.addWidget(self.main_content)
        self.main_splitter.setSizes([60, 250, 850])

        # Variables for selected segment
        self.selected_start = None
        self.selected_end = None

        # Connect row selection
        self.table.selectionModel().selectionChanged.connect(self.on_row_selection)
        
        # Center the window
        self.center_window()

    def setup_display_options(self):
        """Set up the display options section with combo box"""
        options_layout = QHBoxLayout()
        
        # Create label for combo box
        options_label = QLabel("Display Options:", self)
        options_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        # Create combo box
        self.display_combo = QComboBox(self)
        self.display_combo.addItems(["Transcription Only", "Translation Only", "Both"])
        self.display_combo.setCurrentText("Transcription Only")  # Default selection
        self.display_combo.currentTextChanged.connect(self.update_table_columns)
        
        # Add widgets to layout
        options_layout.addWidget(options_label)
        options_layout.addWidget(self.display_combo)
        options_layout.addStretch()
        
        self.layout.addLayout(options_layout)

    def setup_table(self):
        """Set up the table widget with initial columns"""
        self.table = QTableWidget()
        self.table.setRowCount(len(self.segments))
        self.update_table_columns()
        
        # Add the table to a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.table)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

    def update_table_columns(self):
        """Update table columns based on combo box selection"""
        display_option = self.display_combo.currentText()
        
        # Determine columns based on selection
        if display_option == "Transcription Only":
            columns = ["Start", "End", "Transcription"]
        elif display_option == "Translation Only":
            columns = ["Start", "End", "Translation"]
        else:  # Both
            columns = ["Start", "End", "Transcription", "Translation"]
            
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Populate the table
        for row, entry in enumerate(self.segments):
            # Add start and end times
            self.table.setItem(row, 0, QTableWidgetItem(str(entry["start"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry["end"])))
            
            # Add transcription and/or translation based on selection
            if display_option in ["Transcription Only", "Both"]:
                transcription_col = 2 if display_option == "Transcription Only" else 2
                self.table.setItem(row, transcription_col, QTableWidgetItem(entry["text"]))
                
            if display_option in ["Translation Only", "Both"]:
                translation_col = 2 if display_option == "Translation Only" else 3
                translation = entry.get("translation", "")  # Get translation if available
                self.table.setItem(row, translation_col, QTableWidgetItem(translation))

        # Resize columns and rows
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def create_toolbar(self):
        """Creates the toolbar with View and Export buttons."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Create View Button
        view_action = QAction("View", self)
        toolbar.addAction(view_action)

        # Create View dropdown menu
        self.view_menu = QMenu(self)
        self.view_menu.addAction("Text", self.view_text)
        self.view_menu.addAction("Segments", self.view_segments)

        # Connect View button to open the dropdown
        view_action.triggered.connect(lambda: self.view_menu.exec(toolbar.mapToGlobal(toolbar.actionGeometry(view_action).bottomLeft())))

        # Create Export Button
        export_action = QAction("Export", self)
        toolbar.addAction(export_action)

        # Create Export dropdown menu
        self.export_menu = QMenu(self)
        self.export_menu.addAction("PDF", self.export_pdf)
        self.export_menu.addAction("TXT", self.export_txt)

        # Connect Export button to open the dropdown
        export_action.triggered.connect(lambda: self.export_menu.exec(toolbar.mapToGlobal(toolbar.actionGeometry(export_action).bottomLeft())))

    def view_text(self):
            """Display concatenated text from all segments."""
            display_option = self.display_combo.currentText()
            
            if display_option == "Transcription Only":
                concatenated_text = " ".join(segment["text"] for segment in self.segments)
            elif display_option == "Translation Only":
                concatenated_text = " ".join(segment.get("translation", "") for segment in self.segments)
            else:  # Both
                transcription = " ".join(segment["text"] for segment in self.segments)
                translation = " ".join(segment.get("translation", "") for segment in self.segments)
                concatenated_text = f"Transcription:\n{transcription}\n\nTranslation:\n{translation}"

            # Clear existing widgets from the layout
            self.clear_scroll_area()

            # Create a label to display the text
            text_label = QLabel(concatenated_text, self)
            text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            text_label.setWordWrap(True)
            text_label.setStyleSheet("font-size: 14px; padding: 10px;")
            self.scroll_area.setWidget(text_label)

    def view_segments(self):
        """Switch back to the table view."""
        self.clear_scroll_area()
        self.create_table()
        self.scroll_area.setWidget(self.table)

    def create_table(self):
        """Recreates the table if it's missing."""
        self.table = QTableWidget()
        self.table.setRowCount(len(self.segments))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Start", "End", "Text"])

        for row, entry in enumerate(self.segments):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry["start"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry["end"])))
            self.table.setItem(row, 2, QTableWidgetItem(entry["text"]))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.selectionModel().selectionChanged.connect(self.on_row_selection)

    def clear_scroll_area(self):
        """Clears the current widget in the scroll area."""
        current_widget = self.scroll_area.widget()
        if current_widget:
            current_widget.deleteLater()

    def export_pdf(self):
        """Export data to a PDF (placeholder)."""
        print("Exporting to PDF...")

    def export_txt(self):
        """Export data to a TXT file."""
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "segments.txt",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    for segment in self.segments:
                        file.write(f"Start: {segment['start']} ms\n")
                        file.write(f"End: {segment['end']} ms\n")
                        file.write(f"Text: {segment['text']}\n\n")
                print(f"File saved to: {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")

    def on_audio_player_position_ms_changed(self, position_ms: int) -> None:
        current_segment = [
            segment
            for segment in self.segments
            if segment.get("start") <= position_ms < segment.get("end")
        ]

        if current_segment:
            display_option = self.display_combo.currentText()
            if display_option == "Translation Only":
                text = current_segment[0].get("translation", "")
            elif display_option == "Both":
                trans = current_segment[0].get("text", "")
                transl = current_segment[0].get("translation", "")
                text = f"{trans}\n{transl}"
            else:  # Transcription Only
                text = current_segment[0].get("text", "")
            self.subtitle_label.setText(text)
        else:
            self.subtitle_label.setText("")

        if self.selected_start is not None and self.selected_end is not None:
            if position_ms >= self.selected_end:
                self.audio_player.set_position(self.selected_start)

    def reset_playback(self):
        """Reset playback to normal mode."""
        self.selected_start = None
        self.selected_end = None
        print("Playback reset to normal mode.")

    def on_row_selection(self):
        """Handles row selection in the table and sets the start and end times."""
        selected_row = self.table.selectedIndexes()
        if selected_row:
            row = selected_row[0].row()
            self.selected_start = self.segments[row]["start"]
            self.selected_end = self.segments[row]["end"]
            print(f"Segment selected: {self.selected_start} ms to {self.selected_end} ms")
            self.audio_player.set_position(self.selected_start)

    def toggle_summary_panel(self):
        """Collapse or show the summary panel."""
        if self.summary_panel.isVisible():
            self.summary_panel.hide()
            self.main_splitter.setSizes([60, 0, 850])
        else:
            self.summary_panel.show()
            self.main_splitter.setSizes([60, 250, 850])

    def open_chatbot_window(self):
        """Open the chatbot UI."""
        self.chatbot_window = ChatBotUI(transcript =self.transcript,
                                        file_path = self.file_path)
        self.chatbot_window.show()

    def center_window(self):
        """Centers the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        window_rect = self.frameGeometry()
        center_point = screen.center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())
