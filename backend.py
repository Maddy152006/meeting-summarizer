import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API key securely from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(file_name, file_bytes):
    """Handles ASR API integration for transcription using Whisper."""
    try:
        transcription = client.audio.transcriptions.create(
            file=(file_name, file_bytes),
            model="whisper-large-v3",
            response_format="text"
        )
        return transcription
    except Exception as e:
        return f"Error during transcription: {str(e)}"

def generate_summary(transcript_text):
    """Uses LLM to summarize transcript into key decisions and tasks."""
    system_prompt = (
        "You are an expert executive meeting assistant. Analyze meeting transcripts "
        "and produce structured, actionable summaries. Always extract:\n"
        "1. Executive Summary\n"
        "2. Key Decisions Made\n"
        "3. Action Items & Tasks (with Assignee/Owner and Deadlines if mentioned)"
    )
    
    user_prompt = f"Summarize this meeting transcript into key decisions and action items:\n\n{transcript_text}"
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def save_meeting_data(filename, transcript, summary):
    """Backend storage logic to save processed data."""
    data = {
        "audio_file": filename,
        "transcript": transcript,
        "summary": summary
    }
    os.makedirs("saved_meetings", exist_ok=True)
    base_name = os.path.splitext(filename)[0]
    file_path = f"saved_meetings/{base_name}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    return file_path