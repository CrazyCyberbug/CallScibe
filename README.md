# Multilingual Audio Transcription & Analysis Application

## Overview
This application enables transcription, entity recognition, and analysis of multilingual audio recordings, specifically targeting Indian languages such as **English, Kannada, Hindi, Tamil, and Malayalam**. With advanced **LLM-based transcription correction**, **timestamped transcriptions**, and an **interactive chatbot**, it provides an intuitive and efficient user experience for analyzing recorded conversations.

## Features
### 1. Multilingual Transcription
- Supports audio transcription for **English, Kannada, Hindi, Tamil, and Malayalam**.
- **Automatic language detection** handles seamless transitions between multiple languages.
- The current prototype supports **Kannada, Tamil, English, and Hindi** with experimental support for **Telugu and Malayalam**.
- **LLM-powered transcription refinement** to enhance accuracy.

### 2. Broad Audio Format Support
- Compatible with all major **audio formats**, ensuring flexibility for diverse use cases.

### 3. Timestamped Transcriptions
- Each transcription **includes a start and end timestamp** for easy navigation.
- Allows precise correction, review, and **analysis of key conversation points**.

### 4. Looping Audio Segments
- Users can loop specific sections of audio for focused review.
- Ideal for **detailed transcription analysis, corrections, and verification**.

### 5. Named Entity Recognition (NER)
- Automatically **extracts and highlights key information**, such as:
  - **Names** (People mentioned in the conversation)
  - **Places** (Geographical references)
  - **Organizations** (Companies, institutions, etc.)
  - **Date & Time** (Temporal references for context)
- Uses **color-coded highlighting** for easier readability and analysis.

### 6. Chatbot for Interactive Analysis
- **AI-powered assistant** that allows users to ask questions about the transcription.
- Enables **searching for entities, speech pattern analysis, and insightful queries**.
- Provides **accurate answers with context retrieved from transcripts**.

## User Interface Walkthrough
### Home Screen
- Displays **previously transcribed audio files**.
- Toolbar options to **add, delete, and view** transcriptions.

### Transcription Window
#### Segments Viewer and Audio Player
- Interactive table displaying transcribed **text alongside timestamps**.
- **Audio player syncs with transcription text**, functioning like subtitles.
- Clicking a row **loops the corresponding audio segment** for in-depth analysis.

#### Summary Panel and Sidebar
- **Collapsible panel** provides an **overview of transcriptions** at a glance.
- Sidebar contains:
  - **Expand/collapse summary panel**
  - **Open chatbot**
  - **Run Named Entity Recognition (NER)**

### Named Entity Recognition (NER)
- Extracts **names, places, dates, and organizations** in a **color-coded** format.
- Includes a **legend to help users interpret entity types**.

### Chatbot
- **Conversational AI-powered assistant** to analyze transcriptions.
- Provides **fact-based responses** using transcript data.

## Installation & Setup
### Prerequisites
Ensure your system meets the **minimum requirements** mentioned above.

### Installation Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/multilingual-audio-transcription.git
   cd multilingual-audio-transcription
   ```
2. **Set up a virtual environment and install dependencies:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```sh
   python app.py
   ```
4. **Access the application** by navigating to `http://localhost:5000/` in your browser.

## Usage Guide
- **Upload an audio file** via the home screen.
- **Start transcription** and wait for processing.
- **Use NER and chatbot** for deeper analysis.
- **Loop audio segments** for verification.

## Demo
[Click here for a video demonstration](https://drive.google.com/file/d/1ZxJViKk4DD2OaOwOXwWiGpqEHG9ELhnN/view?usp=sharing)

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch-name`).
3. Commit changes and push to your branch.
4. Submit a Pull Request for review.

## License
This project is licensed under the **MIT License**.

---
For any issues or queries, please **raise an issue** in the GitHub repository or contact the maintainers.

Happy transcribing! 🎤

