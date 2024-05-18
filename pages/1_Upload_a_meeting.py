# Import libraries
import streamlit as st
from transformers import pipeline
import time
from datetime import datetime
from streamlit_js_eval import get_page_location

# Set the page configuration
st.set_page_config(
    page_title="ArcticMeet – Upload a meeting",
    page_icon="❄️",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/rokbenko/arctic-meet",
    },
)

# Add a sidebar
with st.sidebar:
    # Add a copyright and social media links
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )

    # Add "Powered by Snowflake" logo
    st.markdown("<div>&nbsp;</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
    with col1:
        st.write("&nbsp;")
    with col2:
        st.image("powered_by_snowflake_stacked_white.png", use_column_width=True)
    with col3:
        st.write("&nbsp;")

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
            <p style='text-align: center; margin-bottom: 0.5rem;'>
                Start by uploading your meeting so that ArcticMeet can get a transcription of it. ArcticMeet needs a transcription, which is a written version of what was said in your meeting. This helps ArcticMeet understand and analyze your meeting in the next steps.
            </p>
        """,
        unsafe_allow_html=True,
    )

    # Get the URL of the current page
    get_url = get_page_location()
    if get_url is not None:
        get_url_host = get_url.get("host")

        # If user uses the publicly available version of ArcticMeet hosted on Streamlit Cloud, show an important privacy notice
        if get_url_host == "arctic-meet.streamlit.app":
            st.error(
                body="""
                        #### ⚠️ Important privacy notice ⚠️

                        Please be aware that you're currently using the publicly available version of ArcticMeet hosted on Streamlit Cloud, meaning that all transcriptions of meetings you upload here can be viewed by anyone in the world. Do not upload any sensitive or private meetings in any way.

                        I strongly recommend you use the provided sample meeting, which is a simulated, dummy meeting designed for testing purposes.

                        By proceeding, you acknowledge and understand the risks associated with uploading meetings to ArcticMeet. You absolve ArcticMeet and its developers of any responsibility for the consequences of such uploads.

                        Thank you for your attention to this matter.
                    """,
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
                Don't you have your own meeting to try? Download and try a [sample meeting](https://github.com/rokbenko/arctic-meet/blob/main/sample_meeting.mp4?raw=true).
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
                label=f"Getting a transcription of {uploaded_meeting.name}... This could take a while. Please be patient.",
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

                    # Use cache to transcribe the uploaded meeting only once if the user keeps uploading the same meeting
                    # The transcription will be cached for 1 hour
                    @st.cache_resource(
                        ttl=3600,
                        show_spinner="ArcticMeet is caching the transcription...",
                    )
                    def load_model(transcription):
                        pipe = pipeline(
                            "automatic-speech-recognition", "openai/whisper-tiny"
                        )

                        return pipe(transcription)

                    # Transcribe the uploaded meeting
                    transcription = load_model(bytes_data)

                    step3_time = int((time.time() - start_time) * 1000)
                    with col1:
                        st.write("Transcription got ✔️")
                    with col2:
                        st.write(format_time(step3_time))

                    # Update the status container after the transcription is obtained
                    status.update(
                        label=f"ArcticMeet successfully got a transcription of {uploaded_meeting.name}",
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


if __name__ == "__main__":
    # Run the main function
    main()
