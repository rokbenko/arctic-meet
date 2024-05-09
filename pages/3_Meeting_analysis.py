# Import libraries
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – Meeting analysis",
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

# Add a custom CSS for the selected transcription text
st.markdown(
    """
        <style>
            .selected-transcription {
                color: #29B5E8;
            }
        </style>""",
    unsafe_allow_html=True,
)


# Define the main function
def main():
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
            show_selected_transcription = st.session_state["selected_transcription"]

            # Add a text box to display the selected transcription
            st.markdown(
                f"""
                    <div style='text-align:center;'>You selected the following transcription to analyze:</div>
                    <div class='selected-transcription' style='text-align:center; margin-bottom: 2rem;'>{show_selected_transcription}</div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.button(
                    "Start transcription analysis",
                    use_container_width=True,
                    type="secondary",
                )
            with col2:
                st.button(
                    "Stop transcription analysis",
                    use_container_width=True,
                    type="primary",
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
                cta_button = st.button("Go back to Step 2", use_container_width=True)
            with col3:
                st.write("&nbsp;")

            if cta_button:
                st.switch_page("pages/2_Select_a_transcription.py")

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
            cta_button = st.button("Start using ArcticAlly", use_container_width=True)
        with col3:
            st.write("&nbsp;")

        # If the CTA button is clicked, switch pages
        if cta_button:
            st.switch_page("pages/1_Upload_a_meeting.py")

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
