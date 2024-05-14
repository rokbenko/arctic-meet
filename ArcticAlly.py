# Import libraries
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="ArcticAlly – AI meeting assistant, always on your side 🙌",
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
    # Add a title and subtitle
    st.markdown(
        """
            <h1 style='text-align: center;'>❄️ ArcticAlly ❄️</h1>
            <h4 style='text-align: center; margin-bottom: 0.5rem;'>AI meeting assistant,<br> always on your side 🙌</h4>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div style='width: 100%; text-align: center; margin-bottom: 1rem;'>👉 Give ArcticAlly a ⭐ star on <a href='https://github.com/rokbenko/arctic-ally'>GitHub</a>. 👈</div>""",
        unsafe_allow_html=True,
    )

    # Add a description
    st.write(
        "Introducing ArcticAlly, your AI meeting assistant powered by Snowflake. Developed for the Snowflake June 2024 hackathon, ArcticAlly offers comprehensive meeting analysis with a suite of advanced features. From summarization to agenda extraction, participant identification, sentiment analysis, and translation capabilities, ArcticAlly empowers you to effortlessly uncover valuable insights. With an intuitive Streamlit GUI and seamless integration of cutting-edge technologies, especially the Snowflake Arctic LLM, ArcticAlly revolutionizes your meeting experience."
    )

    # Add a CTA button to continue with Step 1
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("&nbsp;")
    with col2:
        cta_button = st.button(
            "Start using ArcticAlly 🚀", type="primary", use_container_width=True
        )
    with col3:
        st.write("&nbsp;")

    # If the CTA button is clicked, switch pages
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
