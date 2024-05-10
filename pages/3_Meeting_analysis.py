# Import libraries
import streamlit as st
from snowflake.snowpark import Session
from snowflake.cortex import Summarize, Complete
import pandas as pd

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


def analyze_transcription(selected_transcription_value):
    # Summary
    summary = Summarize(text=selected_transcription_value, session=session)

    # Keywords
    keywords = Complete(
        model="snowflake-arctic",
        prompt=f"Give me up to 5 keywords of the following text: {selected_transcription_value}. Your response should be in JSON format.",
        session=session,
    )

    return summary, keywords


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

                # Add a text box to display the selected transcription
                st.markdown(
                    f"""
                        <div style='text-align:center;'>You selected the following transcription to analyze:</div>
                        <div class='selected-transcription' style='text-align:center; margin-bottom: 2rem;'>{selected_transcription_key}</div>
                    """,
                    unsafe_allow_html=True,
                )

                # Buttons to start and stop the transcription analysis
                col_start, col_stop = st.columns(2)
                with col_start:
                    start_button = st.button(
                        "Start transcription analysis",
                        use_container_width=True,
                        type="secondary",
                    )
                with col_stop:
                    stop_button = st.button(
                        "Stop transcription analysis",
                        use_container_width=True,
                        type="primary",
                    )

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
                    selected_transcription_value = transcription_df.loc[
                        index[0], "Value"
                    ]

                if start_button:
                    analysis_result = analyze_transcription(
                        selected_transcription_value
                    )
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
                    "Start using ArcticAlly", use_container_width=True
                )
            with col3:
                st.write("&nbsp;")

            # If the CTA button is clicked, switch pages
            if cta_button:
                st.switch_page("pages/1_Upload_a_meeting.py")

        if analysis_result:
            # Add tabs to display the different sections of the analysis
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
                st.header("Summary of the meeting")
                if analysis_result:
                    summary, keywords = analysis_result

                    if summary:
                        st.write(summary)
                    else:
                        st.write("No summary available")
                    if keywords:
                        st.text("Keywords: " + keywords)
                    else:
                        st.write("No keywords available")
                else:
                    st.write("No meeting analysis available")

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
