# Import libraries
import streamlit as st
from transformers import pipeline
import time
from datetime import datetime

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – Upload a meeting",
    page_icon="❄️",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/rokbenko/arctic-ally",
    },
)

# Add a custom CSS for the start and stop buttons
st.markdown(
    """
        <style>
            div[data-testid="column"]:nth-of-type(1) button {
                width: 100%;
            }

            div[data-testid="column"]:nth-of-type(2) button {
                width: 100%;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

# Add a custom CSS for the sidebar
st.markdown(
    """
        <style>
            [data-testid=stSidebar] {
                background: linear-gradient(0deg, rgba(41,181,232,1) 0%, rgba(17,86,127,1) 100%);
            }

            [data-testid="stSidebarNavItems"]::before {
                background-image: linear-gradient(0deg, transparent, #11567f)
            }

            [data-testid="stSidebarNavItems"]::after {
                background-image: linear-gradient(180deg, transparent, #11567f)
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
    # Add a title
    st.markdown(
        """
            <h2 style='text-align: center; margin-bottom: 0.5rem;'>❄️ Step 1: Upload a meeting ❄️</h2>
            <p style='text-align: center; margin-bottom: 2rem;'>
                Start by uploading your meeting so that ArcticAlly can get a transcription of it. ArcticAlly needs a transcription, which is a written version of what was said in your meeting. This helps ArcticAlly understand and analyze your meeting in the next steps.
            </p>
        """,
        unsafe_allow_html=True,
    )

    # Create the form for the user to upload a meeting
    with st.form(key="upload_form"):
        # File uploader
        uploaded_meeting = st.file_uploader(
            label="Upload your meeting to get a transcription of it",
            type=["mp4"],
            accept_multiple_files=False,
            help="You can only upload one meeting at a time. The file must be in mp4 format and not larger than 5GB.",
        )

        # Info message with a link to the sample meeting
        st.info(
            """
                Don't you have your own meeting to try? Download and try a [sample meeting](https://github.com/rokbenko/arctic-ally/blob/main/sample_meeting.mp4?raw=true).
            """
        )

        # Buttons to start and stop getting a transcription
        col_start, col_stop = st.columns([0.2, 0.2])
        with col_start:
            start_button = st.form_submit_button(
                label="Start getting a transcription",
                type="secondary",
            )
        with col_stop:
            stop_button = st.form_submit_button(
                label="Stop getting a transcription", type="primary"
            )

        if start_button and uploaded_meeting is not None:
            # If the start button is clicked and there is a meeting uploaded, start getting a transcription
            # Initialize the start time
            start_time = time.time()

            # Add a status container to show the progress of getting a transcription
            with st.status(
                label=f"Getting a transcription of {uploaded_meeting.name}... This could take a few minutes. Please be patient.",
                expanded=True,
            ) as status:
                col1, col2 = st.columns([0.9, 0.1])

                # Step 1: Looking for uploaded meeting
                with col1:
                    st.write("Looking for uploaded meeting...")
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

                    # Step 3: Getting a transcription of uploaded meeting
                    with col1:
                        st.write("Getting a transcription of uploaded meeting...")
                    with col2:
                        st.write("&nbsp;")

                    pipe = pipeline(
                        "automatic-speech-recognition", "openai/whisper-large-v3"
                    )
                    transcription = pipe(bytes_data)  # Transcribe the uploaded meeting

                    step3_time = int((time.time() - start_time) * 1000)
                    with col1:
                        st.write("Transcription got ✔️")
                    with col2:
                        st.write(format_time(step3_time))

                    # Update the status container after the transcription is obtained
                    status.update(
                        label=f"ArcticAlly successfully got a transcription of {uploaded_meeting.name}",
                        expanded=False,
                    )

                    # Store the transcription to the session state
                    get_time = datetime.fromtimestamp(time.time()).strftime(
                        "%Y-%m-%d_%H:%M:%S"
                    )
                    if f"transcription_{get_time}" not in st.session_state:
                        st.session_state[f"transcription_{get_time}"] = transcription[
                            "text"
                        ]

            # If the stop button is clicked, stop getting a transcription
            if stop_button:
                st.stop()

        if start_button and uploaded_meeting is None:
            # If the start button is clicked and there is no meeting uploaded, show a toast notification
            st.toast(
                body="There is no meeting uploaded to start getting a transcription. Please upload a meeting.",
                icon="❌",
            )

        if stop_button and uploaded_meeting is None:
            # If the stop button is clicked and there is no meeting uploaded, show a toast notification
            st.toast(
                body="Getting a transcription can be stopped only after starting it.",
                icon="❌",
            )

    # Get keys starting with "transcription_"
    transcription_keys = [
        key for key in st.session_state.keys() if key.startswith("transcription_")
    ]

    # Add a CTA button to continue with Step 2
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("&nbsp;")
    with col2:
        cta_button = st.button(
            label="Continue with Step 2 🚀",
            type="secondary",
        )
    with col3:
        st.write("&nbsp;")

    # If the CTA button is clicked
    if cta_button:
        if transcription_keys:
            # If there are transcription keys, switch pages
            st.switch_page("pages/2_Select_a_transcription.py")
        else:
            # If there are no transcription keys, show a toast notification
            st.toast(
                body="There is no meeting uploaded to continue with Step 2. Please upload a meeting.",
                icon="❌",
            )

    # Add a sidebar
    with st.sidebar:
        # Add a copyright notice and social media links at the bottom of the sidebar
        st.markdown(
            """
                <div style='height: calc(100vh - 220px - 1rem - 6rem); display: flex;'>
                    <div style='flex-grow: 1; justify-content: center; display: flex; align-items: end;'>
                        <div style='text-align: center; padding: 1rem 2rem; background-color: rgb(14, 17, 23); border-radius: 0.5rem;'>
                            <div style='margin-bottom: 0.5rem;'>
                                Made with ❤️ by Rok Benko
                            </div>
                            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
                            <a href="https://www.linkedin.com/in/rokbenko/" style='text-decoration: none;'>
                                <i style='color: #0072B1; margin-right: 1rem;' class="fa-xl fa-brands fa-linkedin"></i>
                            </a>
                            <a href="https://stackoverflow.com/users/10347145/rok-benko?tab=profile" style='text-decoration: none;'>
                                <i style='color: #F48024; margin-right: 1rem;' class="fa-xl fa-brands fa-stack-overflow"></i>
                            </a>
                            <a href="https://github.com/rokbenko" style='text-decoration: none;'>
                                <i style='color: #FFFFFF; margin-right: 1rem;' class="fa-xl fa-brands fa-github"></i>
                            </a>
                            <a href="https://www.youtube.com/@CodeAIwithRok" style='text-decoration: none;'>
                                <i style='color: #FF0000; margin-right: 1rem;' class="fa-xl fa-brands fa-youtube"></i>
                            </a>
                            <a href="https://www.patreon.com/rokbenko" style='text-decoration: none;'>
                                <i style='color: #F96854;' class="fa-xl fa-brands fa-patreon"></i>
                            </a>
                        </div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    # Run the main function
    main()
