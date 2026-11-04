import os
import shutil
import tempfile
import streamlit as st

from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.sammarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.vector_store import build_vector_store
from core.rag_engine import build_rag_chain, load_rag_chain

load_dotenv()

CHROMA_DIR = "vector_db"


def save_uploaded_file(uploaded_file):
    """Save Streamlit's uploaded file so process_input() can read its path."""
    os.makedirs("uploads", exist_ok=True)
    suffix = os.path.splitext(uploaded_file.name)[1] or ".mp4"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
        dir="uploads",
    ) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return temp_file.name


def create_or_update_rag(transcript: str, database_action: str):
    """
    overwrite: remove the old Chroma directory, then create a fresh database.
    extend: add this transcript to the existing Chroma collection.
    """
    if database_action == "Overwrite existing database":
        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR)

        return build_rag_chain(transcript)

    if database_action == "Extend existing database":
        # Chroma.from_documents adds the new transcript chunks to the
        # existing collection. Then create a retriever over the updated DB.
        build_vector_store(transcript)
        return load_rag_chain()

    # No existing database: create the first database.
    return build_rag_chain(transcript)

def run_streamlit_pipeline(source: str, language: str, database_action: str):
    """Run the same processing stages used by the command-line pipeline."""
    st.write("### Processing your meeting")

    with st.status("Processing meeting...", expanded=True) as status:
        st.write("1. Extracting audio and creating chunks...")
        chunks = process_input(source)

        st.write("2. Transcribing audio...")
        transcript = transcribe_all(chunks, language)

        if not transcript.strip():
            raise ValueError("No speech was detected in the provided audio.")

        st.write("3. Generating meeting title...")
        title = generate_title(transcript)

        st.write("4. Creating meeting summary...")
        meeting_summary = summarize(transcript)

        st.write("5. Extracting action items...")
        action_items = extract_action_items(transcript)

        st.write("6. Extracting key decisions...")
        key_decisions = extract_key_decisions(transcript)

        st.write("7. Extracting open questions...")
        questions = extract_questions(transcript)

        st.write("8. Updating the RAG knowledge base...")
        rag_chain = create_or_update_rag(transcript, database_action)

        status.update(label="Meeting processed successfully", state="complete")

    return {
        "title": title,
        "summary": meeting_summary,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "questions": questions,
        "transcript": transcript,
        "rag_chain": rag_chain,
    }

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
)

st.title("🎙️ AI Meeting Assistant")
st.caption("Transcribe meetings, generate summaries, extract decisions and chat with your meeting data.")

if "meeting_result" not in st.session_state:
    st.session_state.meeting_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----- Input section -----
st.header("1. Add a meeting")

source_type = st.radio(
    "Choose meeting source",
    ["YouTube URL", "Upload audio/video"],
    horizontal=True,
)

source = None
uploaded_file = None

if source_type == "YouTube URL":
    source = st.text_input(
        "YouTube video URL",
        placeholder="https://www.youtube.com/watch?v=...",
    ).strip()
else:
    uploaded_file = st.file_uploader(
        "Upload an audio or video file",
        type=["mp3", "wav", "m4a", "mp4", "mov", "mkv", "webm", "mpeg", "mpga"],
    )

language = st.selectbox(
    "Transcription language",
    ["english", "hinglish"],
    help="English uses local Whisper. Hinglish uses the Sarvam speech-to-text-translate API.",
)

# ----- Existing database behavior -----
database_exists = os.path.isdir(CHROMA_DIR)

st.header("2. Existing meeting database")
if database_exists:
    st.info(
        "An existing Chroma database was found. Choose whether to replace it "
        "or add this meeting to it."
    )
    database_action = st.radio(
        "What should happen to the existing data?",
        [
            "Overwrite existing database",
            "Extend existing database",
        ],
        help=(
            "Overwrite deletes the existing vector_db folder and creates a fresh database. "
            "Extend adds this meeting's transcript chunks to the existing collection."
        ),
    )
else:
    st.info("No existing vector database was found. A new database will be created.")
    database_action = "Create new database"

st.warning(
    "When you choose Extend, the RAG chat searches across the old and newly added "
    "meeting transcripts together. Your current vector store does not keep meeting "
    "names as metadata, so retrieved chunks are not automatically separated by meeting."
)

# ----- Process button -----
if st.button("Process meeting", type="primary", use_container_width=True):
    if source_type == "YouTube URL" and not source:
        st.error("Please enter a YouTube URL.")
    elif source_type == "Upload audio/video" and uploaded_file is None:
        st.error("Please upload an audio or video file.")
    else:
        saved_upload_path = None
        try:
            if source_type == "Upload audio/video":
                saved_upload_path = save_uploaded_file(uploaded_file)
                source = saved_upload_path

            result = run_streamlit_pipeline(
                source=source,
                language=language,
                database_action=database_action,
            )

            st.session_state.meeting_result = result
            st.session_state.chat_history = []
            st.success("Your meeting is ready.")
        except Exception as error:
            st.error(f"Processing failed: {error}")
            st.exception(error)
        finally:
            # The original upload is no longer needed after process_input()
            # has created its audio chunks.
            if saved_upload_path and os.path.exists(saved_upload_path):
                os.remove(saved_upload_path)

# ----- Results section -----
result = st.session_state.meeting_result

if result:
    st.divider()
    st.header("3. Meeting results")

    st.subheader("📌 Meeting title")
    st.write(result["title"])

    tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript = st.tabs(
        ["Summary", "Action items", "Key decisions", "Open questions", "Transcript"]
    )

    with tab_summary:
        st.write(result["summary"])

    with tab_actions:
        st.write(result["action_items"])

    with tab_decisions:
        st.write(result["key_decisions"])

    with tab_questions:
        st.write(result["questions"])

    with tab_transcript:
        st.text_area(
            "Full transcript",
            value=result["transcript"],
            height=300,
        )

    st.divider()
    st.header("4. Chat with your meeting database")
    st.caption(
        "Ask questions about this meeting. If you extended an existing database, "
        "answers may also use previously added meetings."
    )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    user_question = st.chat_input("Ask something about the meeting...")
    if user_question:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_question}
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Searching meeting data..."):
                try:
                    answer = result["rag_chain"].invoke(user_question)
                    st.markdown(answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as error:
                    st.error(f"Could not generate an answer: {error}")

elif not database_exists:
    st.caption("Your first meeting will create the vector database.")


