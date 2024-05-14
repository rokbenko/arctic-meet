# Import libraries
import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – Select a transcription",
    page_icon="❄️",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/rokbenko/arctic-ally",
    },
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


# Define the main function
def main():
    # Add a title
    st.markdown(
        "<h2 style='text-align: center; margin-bottom: 0.5rem;'>❄️ Step 2: Select a transcription ❄️</h2>",
        unsafe_allow_html=True,
    )

    # Get keys starting with "transcription_"
    transcription_keys = [
        key for key in st.session_state.keys() if key.startswith("transcription_")
    ]

    if transcription_keys:
        # If there are transcription keys in the session state
        # Add a selectbox to select the transcription to be analyzed
        selected_transcription = st.selectbox(
            "Which transcription would you like to analyze?",
            transcription_keys,
            index=None,
            placeholder="Select a transcription...",
        )

        # Store the selected transcription in the session state
        if "selected_transcription" not in st.session_state:
            st.session_state["selected_transcription"] = selected_transcription
        else:
            st.session_state["selected_transcription"] = selected_transcription

        # Add a CTA button to continue with Step 3
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("&nbsp;")
        with col2:
            cta_button = st.button("Continue with Step 3 🚀", use_container_width=True)
        with col3:
            st.write("&nbsp;")

        # If the CTA button is clicked
        if cta_button:
            selected_transcription = st.session_state.get("selected_transcription")
            if selected_transcription is not None:
                # If a transcription is selected, go to Step 3
                st.switch_page("pages/3_Meeting_analysis.py")
            else:
                # If no transcription is selected, show a toast notification
                st.toast(
                    body="There is no transcription selected. Please select a transcription.",
                    icon="❌",
                )

        # Add a header
        st.markdown("<h3>All past transcriptions</h3>", unsafe_allow_html=True)

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

        # Display the DataFrame using st.data_editor()
        edited_transcription_df = st.data_editor(transcription_df, disabled=True)
    else:
        # If there are no transcription keys in the session state
        # Add an error message
        st.error(
            body="No transcriptions are available to select. Please upload a meeting to get a transcription.",
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

        if cta_button:
            st.switch_page("pages/1_Upload_a_meeting.py")

    # Add "Powered by Snowflake" logo at the bottom
    st.markdown(
        "<div style='margin-bottom: 2rem;'>&nbsp;</div>", unsafe_allow_html=True
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write("&nbsp;")
    with col2:
        st.write("&nbsp;")
    with col3:
        st.image("powered_by_snowflake_stacked_white.png", use_column_width=True)
    with col4:
        st.write("&nbsp;")
    with col5:
        st.write("&nbsp;")

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
