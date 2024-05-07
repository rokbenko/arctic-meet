import streamlit as st
from transformers import pipeline

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – 100%-free AI meeting assistant, always on your side",
    page_icon="❄️",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/rokbenko/arctic-ally",
        "About": "# Lorem ipsum",
    },
)


# Define the main function
def main():
    # Set the page title and subtitle
    st.markdown(
        "<h1 style='text-align: center;'>❄️ ArcticAlly ❄️</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='text-align: center; margin-bottom: 2rem;'>100%-free AI meeting assistant,<br> always on your side 🙌</h4>",
        unsafe_allow_html=True,
    )

    # Create the form for the user to upload a meeting
    with st.form(key="my_form"):
        uploaded_file = st.file_uploader(
            label="Upload a meeting that you would like ArcticAlly to analyze",
            type=["mp4"],
            accept_multiple_files=False,
            help="You can only upload one meeting at a time. The file must be in mp4 format and not larger than 5GB.",
        )

        st.info(
            """
                Don't you have your own meeting to try? Try a sample!
                - Step 1: [Download a sample meeting](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true)
                - Step 2: Upload it using the file uploader above 👆
                - Step 3: Click the "Analyze meeting" button 👇
            """
        )

        submit_button = st.form_submit_button(label="Analyze meeting")

    # Get the transcription of the uploaded meeting
    if uploaded_file is not None:
        if submit_button:
            st.text(f"Analyzing {uploaded_file.name}...")

            bytes_data = uploaded_file.read()

            pipe = pipeline("automatic-speech-recognition", "openai/whisper-large-v2")

            transcription = pipe(bytes_data)

            st.write("Transcription:")
            st.write(transcription)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "Summary",
            "Todo",
            "Participants",
            "Sentiment",
            "Translation",
            "Insights",
            "Integrations",
            "Follow-ups",
        ]
    )

    with tab1:
        st.header("Summary")
        st.text("Summary: ...")
        st.text("Keywords: ...")

    with tab2:
        st.header("Todo")

    with tab3:
        st.header("Participants")

    with tab4:
        st.header("Sentiment")

    with tab5:
        st.header("Translation")

    with tab6:
        st.header("Insights")

    with tab7:
        st.header("Integrations")

    with tab8:
        st.header("Follow-ups")

    # Create the sidebar
    with st.sidebar:
        st.title("Past meetings")


if __name__ == "__main__":
    # Run the main function
    main()
