import sys
import os
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QTextEdit,
                             QLineEdit,
                             QPushButton,
                             QHBoxLayout)

from LLM.ConversationManager import ConversationManager, simple_prompt, call_assistant_prompt, transcript

welcome_text = "Hello! I’m your AI assistant, ready to help you analyze transcripts from {file_name}. Let’s get started!"

class ChatBotUI(QWidget):
    def __init__(self, transcript, file_path):
        super().__init__()
        self.file_path = file_path
        self.transcript = transcript
        self.init_ui()
        self.system_prompt = simple_prompt
        self.conversation_manager = ConversationManager(system_prompt = call_assistant_prompt.format(call_transcript = self.transcript))

    def init_ui(self):
        self.setWindowTitle("Chat Window")
        self.setGeometry(100, 100, 500, 400)

        # Layout
        layout = QVBoxLayout()

        # Chat display (Read-only)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input field
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Send")

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        # Event handling
        self.send_button.clicked.connect(self.process_input)
        self.input_field.returnPressed.connect(self.process_input)  # Enter key support    
        formatted_welcome_text = welcome_text.format(file_name = os.path.basename(self.file_path))
        self.chat_display.append(f"<b>User:</b> {formatted_welcome_text}<br>")
        self.setLayout(layout)

    def process_input(self):
        user_text = self.input_field.text().strip()
        if user_text:
            # Bold "User" and add line breaks
            self.chat_display.append(f"<b>User:</b> {user_text}<br>")
            
            response = self.get_response(user_text)
            # Bold "Bot" and add line breaks
            self.chat_display.append(f"<b>Bot:</b> {response}<br>")
            
            self.input_field.clear()

    def get_response(self, user_text):
        response = self.conversation_manager.respond_to_messages(message = user_text)
        return response

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotUI()
    window.show()
    sys.exit(app.exec())
