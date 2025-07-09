import streamlit as st
from youtube_utils import get_transcript_from_url
from blog_writer import generate_blog

# --- Page config ---
st.set_page_config(page_title="YT Video to Blog", page_icon="🎥", layout="centered")

# --- Custom CSS for YouTube-inspired theme ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F9F9F9;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #FF0000;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border: 1px solid #CCCCCC;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("<h1 style='color: #FF0000;'>🎥 YouTube Video to Blog Generator</h1>", unsafe_allow_html=True)
st.markdown("Convert any YouTube video into a blog post using GenAI 🧠")

# --- Input Section ---
youtube_link = st.text_input("🔗 Paste YouTube Video Link")

output_type = st.radio(
    "🧾 Choose Output Type:",
    ["Blog Post", "Summary", "LinkedIn-style"]
)

tone = st.radio(
    "🎨 Choose Tone:",
    ["Professional", "Friendly", "SEO Optimized"]
)

# --- Generate Button ---
if st.button("🚀 Generate Blog"):
    if youtube_link.strip() == "":
        st.warning("Please paste a YouTube link first.")
    else:
        # Get Transcript
        transcript_text = get_transcript_from_url(youtube_link)

        if transcript_text.startswith("⚠️") or transcript_text.startswith("❌"):
            st.error(transcript_text)
        else:
            st.success("✅ Transcript fetched! Generating blog...")
            
            # Generate blog using AI
            blog_result = generate_blog(transcript_text, output_type, tone)
            
            # Show result
            st.markdown("### 📝 Generated Blog Post")
            st.text_area("Your blog post:", blog_result, height=400)

            # Actions
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="⬇️ Download as .txt",
                    data=blog_result,
                    file_name="generated_blog.txt",
                    mime="text/plain"
                )
            with col2:
                st.code(blog_result[:500] + "..." if len(blog_result) > 500 else blog_result, language="markdown")