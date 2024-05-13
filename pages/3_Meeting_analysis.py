# Import libraries
import streamlit as st
from snowflake.snowpark import Session
from snowflake.cortex import Summarize, Complete, Sentiment, Translate
import pandas as pd
import json
import re

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – Meeting analysis",
    page_icon="❄️",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/rokbenko/arctic-ally",
    },
)

# Define Snowflake connection parameters
connection_params = {
    "account": st.secrets.get("SNOWFLAKE_ACCOUNT"),
    "user": st.secrets.get("SNOWFLAKE_USER_NAME"),
    "password": st.secrets.get("SNOWFLAKE_USER_PASSWORD"),
}

if (
    not connection_params["account"]
    or not connection_params["user"]
    or not connection_params["password"]
):
    st.sidebar.write(
        "#### ArcticAlly uses Snowflake Cortex to analyze meetings. Please set your Snowflake credentials below."
    )

# If account is not set in the secrets, ask the user to set it in the sidebar
if not connection_params["account"]:
    account_from_input = st.sidebar.text_input(
        label="Set your Snowflake account here:",
        placeholder="xxxxxxx-xxxxxxx",
        type="default",
    )
    if account_from_input:
        connection_params["account"] = account_from_input

# If user is not set in the secrets, ask the user to set it in the sidebar
if not connection_params["user"]:
    user_from_input = st.sidebar.text_input(
        label="Set your Snowflake user here:",
        placeholder="john_doe",
        type="default",
    )
    if user_from_input:
        connection_params["user"] = user_from_input

# If password is not set in the secrets, ask the user to set it in the sidebar
if not connection_params["password"]:
    password_from_input = st.sidebar.text_input(
        label="Set your Snowflake password here:",
        placeholder="donttellanyone123",
        type="password",
    )
    if password_from_input:
        connection_params["password"] = password_from_input

# Initialize session variable to None, so in case at least one secret is not set, the finally block will not throw an error "NameError: name 'session' is not defined"
session = None

# Create Snowflake session
if (
    connection_params["account"]
    and connection_params["user"]
    and connection_params["password"]
):
    session = Session.builder.configs(connection_params).create()

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

# Add a custom CSS for the selected transcription text
st.markdown(
    """
        <style>
            .selected-transcription {
                color: #29B5E8;
            }
        </style>
    """,
    unsafe_allow_html=True,
)


# Define a function to get the selected transcription value from the session state
def get_transcription_value(selected_transcription_key):
    # Prepare the selected transcription value for analysis
    # Create an empty DataFrame to store the transcription key-value pairs
    transcription_data = {"Key": [], "Value": []}

    # Iterate over the keys in the session state
    for key in st.session_state.keys():
        # Check if the key starts with "transcription_"
        if key.startswith("transcription_"):
            # If a key starts with "transcription_", add the key-value pair to the DataFrame
            transcription_data["Key"].append(key)
            transcription_data["Value"].append(st.session_state[key])

    # Convert the dictionary to a DataFrame
    transcription_df = pd.DataFrame(transcription_data)

    # Find the index of the row where the Key matches selected_transcription_key
    index = transcription_df.index[
        transcription_df["Key"] == selected_transcription_key
    ].tolist()

    # If there's a match
    if index:
        # Save the selected transcription value for analysis
        selected_transcription_value = transcription_df.loc[index[0], "Value"]

    return selected_transcription_value


# Define a function to analyze the selected transcription
def analyze_transcription(
    selected_transcription_value,
    summary_checkbox,
    agenda_checkbox,
    participants_checkbox,
    sentiment_checkbox,
    translation_checkbox,
    selected_from_language,
    selected_to_language,
    insights_checkbox,
):
    # Initialize variables to store analysis results
    summary = None
    keywords = None
    agenda = None
    participants = None
    sentiment_df = pd.DataFrame()
    translation = None
    insights = None

    # If the summary checkbox is checked
    if summary_checkbox:
        summary = Summarize(text=selected_transcription_value, session=session)

        keywords = Complete(
            model="snowflake-arctic",
            prompt=f'Give me up to five keywords from the following text in a JSON object containing a list of keywords: {selected_transcription_value}. Your response should be in JSON format, not in a list or any other format. Here you have an example of the response: {{"keywords": ["keyword1","keyword2","keyword3","keyword4","keyword5"]}}',
            session=session,
        )

    # If the agenda checkbox is checked
    if agenda_checkbox:
        agenda = Complete(
            model="snowflake-arctic",
            prompt=f"Give me a concise agenda with a maximum of five topics discussed in the following text: {selected_transcription_value}. Your response should be a numbered list. Here you have an example of the response: 1. Topic 1\n2. Topic 2\n3. Topic 3\n4. Topic 4\n5. Topic 5",
            session=session,
        )

    # If the participants checkbox is checked
    if participants_checkbox:
        participants = Complete(
            model="snowflake-arctic",
            prompt=f"Give me a list of participants if you can extract names in the following text: {selected_transcription_value}. Your response should be a list. Here you have an example of the response if you can extract names: 1. John Doe\n2. Jane Doe\n3. Bob Smith. If you cannot extract names, return just a number of participants. Here you have an example of the response if you cannot extract names: There were 3 participants in the meeting.",
            session=session,
        )

    # If the sentiment checkbox is checked
    if sentiment_checkbox:
        sentences = re.split(
            r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", selected_transcription_value
        )

        # Create a list to store sentiment data
        sentiment_data = []

        # Iterate over each sentence and calculate sentiment
        for sentence in sentences:
            sentiment = Sentiment(text=sentence, session=session)
            # Append the sentiment data to the list
            sentiment_data.append({"Sentence": sentence, "Sentiment": sentiment})

        # Convert the list of dictionaries into a DataFrame
        sentiment_df = pd.DataFrame(sentiment_data)

    # If the translation checkbox is checked
    if translation_checkbox:
        translation = Translate(
            text=selected_transcription_value,
            from_language=selected_from_language,
            to_language=selected_to_language,
            session=session,
        )

    # If the insights checkbox is checked
    # Todo

    return summary, keywords, agenda, participants, sentiment_df, translation, insights


# Languages that are supported for the Translate function
languages_supported = [
    "English",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Polish",
    "Portuguese",
    "Russian",
    "Spanish",
    "Swedish",
]


# Define the main function
def main():
    # Initialize analysis_result variable to None
    analysis_result = None

    try:
        # Add a title
        st.markdown(
            "<h2 style='text-align: center; margin-bottom: 0.5rem;'>❄️ Step 3: Meeting analysis ❄️</h2>",
            unsafe_allow_html=True,
        )

        # Get keys starting with "transcription_"
        transcription_keys = [
            key for key in st.session_state.keys() if key.startswith("transcription_")
        ]

        if transcription_keys:
            # If there are transcription keys in the session state
            if "selected_transcription" in st.session_state:
                # If the user has selected a transcription to analyze
                # Get the selected transcription from the session state
                selected_transcription_key = st.session_state["selected_transcription"]

                if selected_transcription_key is not None:
                    # Add a text box to display the selected transcription
                    st.markdown(
                        f"""
                            <div style='text-align:center;'>You selected the following transcription to analyze:</div>
                            <div class='selected-transcription' style='text-align:center; margin-bottom: 1rem;'>{selected_transcription_key}</div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Add a CTA button to go back to Step 2
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("&nbsp;")
                    with col2:
                        cta_button = st.button(
                            "Change the transcription", use_container_width=True
                        )
                    with col3:
                        st.write("&nbsp;")

                    # If the CTA button is clicked, switch pages
                    if cta_button:
                        st.switch_page("pages/2_Select_a_transcription.py")

                    # Create the form for the user to select the analysis options
                    with st.form(key="analysis_form"):
                        # Add a text box to let know the user which analysis options are available
                        st.write(
                            "Please select the analysis options you would like to include:"
                        )

                        # Add checkboxes to select the analysis options
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            summary_checkbox = st.checkbox(
                                "Summary",
                                key="summary_checkbox",
                            )
                        with col2:
                            agenda_checkbox = st.checkbox(
                                "Agenda",
                                key="agenda_checkbox",
                            )
                        with col3:
                            participants_checkbox = st.checkbox(
                                "Participants",
                                key="participants_checkbox",
                            )
                        with col4:
                            sentiment_checkbox = st.checkbox(
                                "Sentiment",
                                key="sentiment_checkbox",
                            )
                        with col1:
                            translation_checkbox = st.checkbox(
                                "Translation",
                                key="translation_checkbox",
                            )
                        with col2:
                            insights_checkbox = st.checkbox(
                                "Insights",
                                key="insights_checkbox",
                            )

                        # Add a selectbox to select the language to translate from and to
                        col_left, col_right = st.columns(2)
                        with col_left:
                            selected_from_language = st.selectbox(
                                "Which language would you like to translate from?:red[*]",
                                languages_supported,
                                index=None,
                                placeholder="Select a language...",
                            )
                            st.write(
                                ":red[* This needs to be the language of your meeting.]"
                            )
                        with col_right:
                            selected_to_language = st.selectbox(
                                "Which language would you like to translate to?",
                                languages_supported,
                                index=None,
                                placeholder="Select a language...",
                            )

                        if selected_from_language == "English":
                            selected_from_language = "en"
                        elif selected_from_language == "French":
                            selected_from_language = "fr"
                        elif selected_from_language == "German":
                            selected_from_language = "de"
                        elif selected_from_language == "Italian":
                            selected_from_language = "it"
                        elif selected_from_language == "Japanese":
                            selected_from_language = "ja"
                        elif selected_from_language == "Korean":
                            selected_from_language = "ko"
                        elif selected_from_language == "Polish":
                            selected_from_language = "pl"
                        elif selected_from_language == "Portuguese":
                            selected_from_language = "pt"
                        elif selected_from_language == "Russian":
                            selected_from_language = "ru"
                        elif selected_from_language == "Spanish":
                            selected_from_language = "es"
                        elif selected_from_language == "Swedish":
                            selected_from_language = "sv"

                        if selected_to_language == "English":
                            selected_to_language = "en"
                        elif selected_to_language == "French":
                            selected_to_language = "fr"
                        elif selected_to_language == "German":
                            selected_to_language = "de"
                        elif selected_to_language == "Italian":
                            selected_to_language = "it"
                        elif selected_to_language == "Japanese":
                            selected_to_language = "ja"
                        elif selected_to_language == "Korean":
                            selected_to_language = "ko"
                        elif selected_to_language == "Polish":
                            selected_to_language = "pl"
                        elif selected_to_language == "Portuguese":
                            selected_to_language = "pt"
                        elif selected_to_language == "Russian":
                            selected_to_language = "ru"
                        elif selected_to_language == "Spanish":
                            selected_to_language = "es"
                        elif selected_to_language == "Swedish":
                            selected_to_language = "sv"

                        # Buttons to start and stop the transcription analysis
                        col_start, col_stop = st.columns(2)
                        with col_start:
                            start_button = st.form_submit_button(
                                "Start transcription analysis",
                                use_container_width=True,
                                type="secondary",
                            )
                        with col_stop:
                            stop_button = st.form_submit_button(
                                "Stop transcription analysis",
                                use_container_width=True,
                                type="primary",
                            )

                        # Run the get_transcription_value function
                        selected_transcription_value = get_transcription_value(
                            selected_transcription_key
                        )

                        # If the start button is clicked
                        if start_button:
                            # If at least one checkbox is checked
                            if (
                                summary_checkbox
                                or agenda_checkbox
                                or participants_checkbox
                                or sentiment_checkbox
                                or translation_checkbox
                                or insights_checkbox
                            ):
                                # If the user has selected the translation checkbox
                                if translation_checkbox:
                                    # If the user has selected a language to translate from and to
                                    if (
                                        selected_from_language
                                        and selected_to_language is not None
                                    ):
                                        # Show a spinner while analyzing the transcription
                                        with st.spinner("Analyzing transcription..."):
                                            # Run the analyze_transcription function
                                            analysis_result = analyze_transcription(
                                                selected_transcription_value,
                                                summary_checkbox,
                                                agenda_checkbox,
                                                participants_checkbox,
                                                sentiment_checkbox,
                                                translation_checkbox,
                                                selected_from_language,
                                                selected_to_language,
                                                insights_checkbox,
                                            )
                                    # If the user has not selected a language to translate from and to, show a toast notification
                                    else:
                                        st.toast(
                                            body="Please select a language to translate from and to.",
                                            icon="❌",
                                        )
                                # If the user has not selected the translation checkbox
                                else:
                                    # Show a spinner while analyzing the transcription
                                    with st.spinner("Analyzing transcription..."):
                                        # Run the analyze_transcription function
                                        analysis_result = analyze_transcription(
                                            selected_transcription_value,
                                            summary_checkbox,
                                            agenda_checkbox,
                                            participants_checkbox,
                                            sentiment_checkbox,
                                            translation_checkbox,
                                            selected_from_language,
                                            selected_to_language,
                                            insights_checkbox,
                                        )
                            else:
                                # If no checkbox is checked
                                # Show a toast notification
                                st.toast(
                                    body="Please select at least one analysis option to analyze.",
                                    icon="❌",
                                )
                else:
                    # EDGE CASE!
                    # If the user has not selected a transcription to analyze
                    # Add an error message
                    st.error(
                        "No transcription is selected to analyze. Please select a transcription to analyze.",
                        icon="❗",
                    )

                    # Add a CTA button to go back to Step 2
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("&nbsp;")
                    with col2:
                        cta_button = st.button(
                            "Select a transcription", use_container_width=True
                        )
                    with col3:
                        st.write("&nbsp;")

                    if cta_button:
                        st.switch_page("pages/2_Select_a_transcription.py")
            else:
                # If the user has not selected a transcription to analyze
                # Add an error message
                st.error(
                    "No transcription is selected to analyze. Please select a transcription to analyze.",
                    icon="❗",
                )

                # Add a CTA button to go back to Step 2
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("&nbsp;")
                with col2:
                    cta_button = st.button(
                        "Go back to Step 2", use_container_width=True
                    )
                with col3:
                    st.write("&nbsp;")

                if cta_button:
                    st.switch_page("pages/2_Select_a_transcription.py")
        else:
            # If there are no transcription keys in the session state
            # Add an error message
            st.error(
                "No transcriptions are available to analyze. Please upload a meeting to get a transcription.",
                icon="❗",
            )

            # Add a CTA button to go back to Step 1
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("&nbsp;")
            with col2:
                cta_button = st.button(
                    "Start using ArcticAlly 🚀", use_container_width=True
                )
            with col3:
                st.write("&nbsp;")

            # If the CTA button is clicked, switch pages
            if cta_button:
                st.switch_page("pages/1_Upload_a_meeting.py")

        if analysis_result:
            # Get the summary, keywords, agenda, participants, sentiment_df, translation and insights from the analysis result
            # Unpack only the non-None values from analysis_result
            (
                summary,
                keywords,
                agenda,
                participants,
                sentiment_df,
                translation,
                insights,
            ) = analysis_result

            # Add a spacer
            st.markdown(
                "<div style='margin-top: 1rem;'>&nbsp;</div>", unsafe_allow_html=True
            )

            # Create a list to store the names of the tabs
            tab_names = []

            # Check if there's a summary and keywords result
            if summary and keywords:
                tab_names.append("Summary")

            # Check if there's an agenda result
            if agenda:
                tab_names.append("Agenda")

            # Check if there's a participants result
            if participants:
                tab_names.append("Participants")

            # Check if there's a sentiment result
            if not sentiment_df.empty:
                tab_names.append("Sentiment")

            # Check if there's a translation result
            if translation:
                tab_names.append("Translation")

            # Check if there's an insights result'
            if insights:
                tab_names.append("Insights")

            # Add tabs only if there are names in the list
            if tab_names:
                st.header("Meeting analysis")

                tabs = st.tabs(tab_names)

                if "Summary" in tab_names:
                    with tabs[tab_names.index("Summary")]:
                        st.subheader("Summary of the meeting")
                        st.write(summary)

                        # Keywords
                        # Parse the JSON string into a dictionary
                        keywords_dict = json.loads(keywords)

                        # Access the "keywords" key in the dictionary
                        get_keywords = keywords_dict["keywords"]

                        # Wrap each keyword with a <span> element
                        keyword_spans = [
                            f"<span>:blue-background[{keyword}]</span>"
                            for keyword in get_keywords
                        ]

                        # Concatenate the <span> elements together
                        keyword_string_with_spans = " ".join(keyword_spans)

                        # Display the keywords with <span> elements
                        st.markdown(
                            f"Keywords: {keyword_string_with_spans}",
                            unsafe_allow_html=True,
                        )
                if "Agenda" in tab_names:
                    with tabs[tab_names.index("Agenda")]:
                        st.subheader("Agenda of the meeting")
                        st.write(agenda)
                if "Participants" in tab_names:
                    with tabs[tab_names.index("Participants")]:
                        st.subheader("Participants of the meeting")
                        st.write(participants)
                if "Sentiment" in tab_names:
                    with tabs[tab_names.index("Sentiment")]:
                        st.subheader("Sentiment of the meeting")
                        st.line_chart(sentiment_df["Sentiment"])
                        st.data_editor(sentiment_df, disabled=True)
                if "Translation" in tab_names:
                    with tabs[tab_names.index("Translation")]:
                        st.subheader("Translation of the meeting")
                        st.write(translation)
                if "Insights" in tab_names:
                    with tabs[tab_names.index("Insights")]:
                        st.subheader("Insights of the meeting")
                        st.write(insights)

    finally:
        if session:
            # Close Snowflake session
            session.close()

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
