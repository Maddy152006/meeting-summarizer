# AI Meeting Summarizer 🎙️

An automated pipeline that transcribes meeting audio/video and generates action-oriented executive summaries, key decisions, and task lists using AI.

## 🚀 Features
* **Speech-to-Text (ASR):** Transcribes audio/video recordings using Groq-hosted `whisper-large-v3`.
* **LLM Action-Oriented Summaries:** Extracts key decisions and structured action items (with owners and deadlines) using `openai/gpt-oss-120b`.
* **Modular Architecture:** Clean separation between UI (`app.py`) and processing/storage logic (`backend.py`).
* **Local Backend Persistence:** Automatically saves processed transcript and summary data to `saved_meetings/` as JSON.
* **Export Artifacts:** Download summaries and transcripts individually (.txt) or as a bundled package (.zip).

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** Python
* **APIs:** Groq Cloud (Whisper-large-v3, GPT-OSS-120B)

## 📦 Local Setup & Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Maddy152006/meeting-summarizer.git](https://github.com/Maddy152006/meeting-summarizer.git)
   cd meeting-summarizer


2. Install required packages:
   ```bash
   pip install -r requirements.txt


3. Set up environment variables:
   Create a .env file in the root directory and add:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here


4. Run the application:
   ```bash
   streamlit run app.py


**Demo Video** (Watch the 1-minute demo walkthrough here) :- https://www.loom.com/share/85df7554f3b14005bb2787a674218010


