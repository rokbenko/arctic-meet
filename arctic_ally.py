import streamlit as st

st.set_page_config(
    page_title="ArcticAlly - Your 100%-free AI meeting assistant",
    page_icon="❄️",
    layout="centered",
    menu_items={
        'Report a bug': "https://github.com/rokbenko/arctic-ally",
        'About': "# Lorem ipsum"
    }
)

st.markdown("<h1 style='text-align: center;'>❄️ ArcticAlly ❄️</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-bottom: 2rem;'>Your 100%-free AI meeting assistant</h4>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(":blue-background[Upload a meeting that you would like ArcticAlly to analyze]", type=["mp4"], accept_multiple_files=False)

if uploaded_file is not None:
    analyze_button = st.button("Analyze")
    if analyze_button:
        st.text("Analyzing...")

def analyze():
    st.text("Analyzing...")