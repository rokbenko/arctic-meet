# Import libraries
import streamlit as st
from transformers import pipeline
import time

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

# Add custom CSS
st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1) button
        {
            width: 100%;
        }

        div[data-testid="column"]:nth-of-type(2) button
        {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Define a function to format the time
def format_time(milliseconds):
    if milliseconds < 1000:
        return f"{int(milliseconds)} ms"
    elif milliseconds < 60000:
        return f"{int(milliseconds/1000)} s"
    else:
        return f"{int(milliseconds/60000)} min"


# Define the main function
def main():
    # Set the page title and subtitle
    st.markdown(
        "<h1 style='text-align: center;'>❄️ ArcticAlly ❄️</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='text-align: center;'>100%-free AI meeting assistant,<br> always on your side 🙌</h4>",
        unsafe_allow_html=True,
    )

    # Create the form for the user to upload a meeting
    with st.form(key="my_form"):
        # File uploader
        uploaded_meeting = st.file_uploader(
            label="Upload a meeting that you would like ArcticAlly to analyze",
            type=["mp4"],
            accept_multiple_files=False,
            help="You can only upload one meeting at a time. The file must be in mp4 format and not larger than 5GB.",
        )

        # Info message with a link to the sample meeting
        st.info(
            """
                Don't you have your own meeting to try? Try a sample!
                - Step 1: [Download a sample meeting](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true)
                - Step 2: Upload it using the file uploader above 👆
                - Step 3: Click the "Start analysis" button below 👇
            """
        )

        col_start, col_stop = st.columns([0.2, 0.2])
        with col_start:
            start_button = st.form_submit_button(
                label="Start analysis", type="secondary"
            )
        with col_stop:
            stop_button = st.form_submit_button(label="Stop analysis", type="primary")

        # If the start button is clicked, start the analysis
        if start_button:
            start_time = time.time()

            # Insert a status container to show the progress of the analysis
            with st.status(
                label=f"Analyzing {uploaded_meeting.name}... This will take a while. Please be patient.",
                expanded=True,
            ) as status:
                col1, col2 = st.columns([0.9, 0.1])

                # Step 1: Searching for uploaded meeting
                with col1:
                    st.write("Searching for uploaded meeting...")
                with col2:
                    st.write("&nbsp;")

                if uploaded_meeting is not None:  # Check if there is a meeting uploaded
                    step1_time = int((time.time() - start_time) * 1000)
                    with col1:
                        st.write("Meeting found ✔️")
                    with col2:
                        st.write(format_time(step1_time))

                    # Step 2: Reading uploaded meeting
                    with col1:
                        st.write("Reading uploaded meeting...")
                    with col2:
                        st.write("&nbsp;")

                    bytes_data = uploaded_meeting.read()  # Read the uploaded meeting

                    step2_time = int((time.time() - start_time) * 1000)
                    with col1:
                        st.write("Meeting read ✔️")
                    with col2:
                        st.write(format_time(step2_time))

                    # Step 3: Making transcription of uploaded meeting
                    with col1:
                        st.write("Making transcription of uploaded meeting...")
                    with col2:
                        st.write("&nbsp;")

                    pipe = pipeline(
                        "automatic-speech-recognition", "openai/whisper-large-v2"
                    )
                    transcription = pipe(bytes_data)  # Transcribe the uploaded meeting

                    step3_time = int((time.time() - start_time) * 1000)
                    with col1:
                        st.write("Transcription made ✔️")
                    with col2:
                        st.write(format_time(step3_time))

        # If the stop button is clicked, stop the analysis
        if stop_button:
            st.stop()

    if "transcription" in locals():
        st.write("Transcription:")
        st.write(transcription["text"])

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
