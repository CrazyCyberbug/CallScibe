from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QComboBox,
    QLabel,
    QPushButton)


supported_language = [
    "English",
    "Hindi",
    "Kannada",
    "Tamil",
]


lang_map = {"English" : "en",
            "Hindi"   : "hi",
            "Kannada" : "kn",
            "Tamil"   : "ta"}



class LanguageSelectionDialog(QDialog):
    """ This is a lan
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Language")
        self.setGeometry(200, 200, 300, 100)
        
        # Layout setup
        layout = QVBoxLayout()
        
        # Label
        self.label = QLabel("Choose a language:")
        layout.addWidget(self.label)
        
        # ComboBox for language selection
        self.combo_box = QComboBox()
        self.combo_box.addItems(supported_language)
        layout.addWidget(self.combo_box)
        
        # OK button to confirm selection
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        # Set layout and initialize dialog
        self.setLayout(layout)
    
    def get_selected_language(self):
        selected_lang = self.combo_box.currentText()
        print(f"Selected Language: {selected_lang}")
        return lang_map[selected_lang]
