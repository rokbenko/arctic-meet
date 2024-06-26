# Import libraries
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="ArcticMeet – AI meeting assistant",
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
                <a href="https://stackoverflow.com/users/10347145/" style='text-decoration: none;'>
                    <i style='color: #F48024; margin-right: 1rem;' class="fa-xl fa-brands fa-stack-overflow"></i>
                </a>
                <a href="https://github.com/rokbenko" style='text-decoration: none;'>
                    <i style='color: #FFFFFF; margin-right: 1rem;' class="fa-xl fa-brands fa-github"></i>
                </a>
                <a href="https://www.youtube.com/@rokbenko?sub_confirmation=1" style='text-decoration: none;'>
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
            <h1 style='text-align: center;'>❄️ ArcticMeet ❄️</h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div style='width: 100%; text-align: center; margin-bottom: 1rem;'>👉 Give ArcticMeet a ⭐ star on <a href='https://github.com/rokbenko/arctic-meet'>GitHub</a>. 👈</div>""",
        unsafe_allow_html=True,
    )

    # Add a description
    st.write(
        "Introducing ArcticMeet, your AI meeting assistant powered by Snowflake. Developed for the Snowflake June 2024 hackathon, ArcticMeet offers comprehensive meeting analysis with a suite of advanced features. From summarization to agenda extraction, participant identification, sentiment analysis, and translation capabilities, ArcticMeet empowers you to effortlessly uncover valuable insights. With an intuitive Streamlit GUI and seamless integration of cutting-edge technologies, especially the Snowflake Arctic LLM, ArcticMeet revolutionizes your meeting experience."
    )

    # Add a CTA button to continue with Step 1
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("&nbsp;")
    with col2:
        cta_button = st.button(
            "Start using ArcticMeet 🚀", type="primary", use_container_width=True
        )
    with col3:
        st.write("&nbsp;")

    # If the CTA button is clicked, switch pages
    if cta_button:
        st.switch_page("pages/1_Upload_a_meeting.py")


if __name__ == "__main__":
    # Run the main function
    main()
