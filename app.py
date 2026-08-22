import streamlit as st
import backend
import zipfile
import io


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="🎙️",
    layout="wide" # Upgraded to wide layout to accommodate the sidebar
)


# SESSION STATE INITIALIZATION

if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'saved_path' not in st.session_state:
    st.session_state.saved_path = None


# USER INTERFACE (SIDEBAR CONTROLS)

with st.sidebar:
    st.header("1. Upload Meeting")
    uploaded_file = st.file_uploader(
        "Select Audio/Video File", 
        type=["mp3", "wav", "m4a", "mp4", "webm", "ogg", "flac", "mpeg", "mpg"]
    )

    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        st.write("---")
        st.header("2. Preview Media")
        if file_ext in ["mp4", "webm"]:
            st.video(uploaded_file)
        else:
            st.audio(uploaded_file)

        st.write("---")
        st.header("3. Generate Insights")
        # Added use_container_width to make the button look cleaner
        process_button = st.button("🚀 Process & Summarize", type="primary", use_container_width=True)
    else:
        process_button = False


# USER INTERFACE (MAIN VIEW)

st.title("🎙️ AI Meeting Summarizer")
st.write(
    "Upload a meeting recording in the sidebar to automatically generate a verbatim "
    "transcript, extract key decisions, and build an action-oriented summary."
)

if uploaded_file is not None and process_button:
    st.session_state.transcript = None
    st.session_state.summary = None

    with st.spinner("Transcribing recording with Whisper ASR..."):
        transcript_result = backend.transcribe_audio(
            uploaded_file.name, 
            uploaded_file.getvalue()
        )

    if transcript_result and not transcript_result.startswith("Error"):
        st.session_state.transcript = transcript_result
        
        with st.spinner("Extracting key decisions and action items with LLM..."):
            summary_result = backend.generate_summary(st.session_state.transcript)

        if summary_result and not summary_result.startswith("Error"):
            st.session_state.summary = summary_result
            st.session_state.saved_path = backend.save_meeting_data(
                uploaded_file.name, 
                st.session_state.transcript, 
                st.session_state.summary
            )
        else:
            st.error(summary_result)
    elif transcript_result:
        st.error(transcript_result)


# RENDER RESULTS

if st.session_state.summary and st.session_state.transcript:
    st.write("---")
    st.success(f"✅ Processing complete! Meeting record securely backed up to `{st.session_state.saved_path}`.")

    tab1, tab2, tab3 = st.tabs(["📋 Summary & Action Items", "📝 Full Transcript", "💾 Export Artifacts"])
    
    with tab1:
        st.markdown(st.session_state.summary)
        
    with tab2:
        st.text_area("Verbatim Transcript", st.session_state.transcript, height=450)
        
    with tab3:
        st.write("### Download Meeting Artifacts")
        st.write("Export your transcript and summary files for offline use.")
        st.write("") # Spacer
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download Summary (.txt)",
                data=st.session_state.summary,
                file_name=f"{uploaded_file.name}_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📥 Download Transcript (.txt)",
                data=st.session_state.transcript,
                file_name=f"{uploaded_file.name}_transcript.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with col3:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(f"{uploaded_file.name}_summary.txt", st.session_state.summary)
                zip_file.writestr(f"{uploaded_file.name}_transcript.txt", st.session_state.transcript)
            
            st.download_button(
                label="📦 Download Both (.zip)",
                data=zip_buffer.getvalue(),
                file_name=f"{uploaded_file.name}_results.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )