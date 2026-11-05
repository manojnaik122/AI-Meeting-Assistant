🎙️ AI Meeting Assistant

An AI-powered meeting assistant that converts audio and video recordings into useful meeting insights. It automatically transcribes meetings, generates summaries, extracts action items and key decisions, and allows users to ask questions about meeting transcripts using Retrieval-Augmented Generation (RAG).

🚀 Features

- Audio & Video Processing: Upload audio/video files or provide a YouTube URL.
- Speech-to-Text: Transcribe English meetings using OpenAI Whisper.
- Hinglish Transcription: Use Sarvam AI for Hinglish transcription.
- Meeting Summarization: Generate concise meeting summaries using an LLM.
- Action Item Extraction: Identify tasks, responsible persons, and deadlines.
- Key Decision Extraction: Extract important decisions made during meetings.
- Open Question Extraction: Identify unresolved questions and follow-up topics.
- AI Meeting Chat: Ask questions about meeting transcripts using RAG.
- Vector Database Management: Create, overwrite, or extend the existing knowledge base.
- Streamlit Interface: Interact with the application through a simple web interface.

🛠️ Technologies Used

Technology| Purpose
Python| Backend development
Streamlit| User interface
OpenAI Whisper| Speech recognition
Sarvam AI| Hinglish transcription
LangChain| LLM orchestration
Groq API| LLM inference
HuggingFace Embeddings| Text embeddings
ChromaDB| Vector database
FFmpeg| Audio processing
Pydub| Audio conversion and chunking
yt-dlp| YouTube audio downloading

🏗️ Project Structure

aimlvedio/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
├── core/
│   ├── transcriber.py
│   ├── sammarize.py
│   ├── extractor.py
│   ├── vector_store.py
│   └── rag_engine.py
│
├── utils/
│   └── audio_processor.py
│
├── downloaders/
├── uploads/
└── vector_db/

Generated folders such as "uploads", "downloaders", and "vector_db" are created during application execution and are excluded from Git.

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AI-Meeting-Assistant.git

2. Navigate to the project directory

cd AI-Meeting-Assistant

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

6. Install FFmpeg

Install FFmpeg and add its "bin" directory to your system PATH.

Verify installation:

ffmpeg -version

7. Configure environment variables

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=saaras:v2.5

Replace the placeholder values with your actual API keys.

Important: Never upload your ".env" file or expose your API keys on GitHub.

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

🔄 Application Workflow

1. Upload an audio/video file or enter a YouTube URL.
2. Select the transcription language.
3. Process the meeting.
4. Generate the meeting title and summary.
5. Extract action items, key decisions, and open questions.
6. Store transcript chunks in ChromaDB.
7. Ask questions about the meeting using the AI chat interface.

🧠 RAG Implementation

The application uses Retrieval-Augmented Generation (RAG) to answer questions based on meeting transcripts.

Workflow:

Meeting Transcript
       |
       v
Text Chunking
       |
       v
HuggingFace Embeddings
       |
       v
ChromaDB Vector Store
       |
       v
Similarity Search
       |
       v
Relevant Context
       |
       v
Groq LLM
       |
       v
Context-Based Answer

📌 Future Improvements

- Meeting-wise transcript organization and retrieval.
- Speaker identification and diarization.
- Downloadable meeting reports in PDF format.
- Improved multilingual transcription support.
- Meeting history and search functionality.

👨‍💻 Author

Manoj

B.Tech – Artificial Intelligence and Machine Learning

---

⭐ If you find this project interesting, consider giving the repository a star!
