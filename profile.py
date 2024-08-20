import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


# Apply custom CSS to remove padding and margins
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .reportview-container .main {
        padding: 0;
    }
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        width: 100%;
        height: 100%;
        border: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        z-index: 999999;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit file uploader
st.title("CSV File Uploader and EDA Report")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding="latin-1")
        
        # Generate the full profiling report
        profile = ProfileReport(df)

        # Save the profiling report
        profile.to_file("test_report.html")
        
        # Load and display the HTML file
        with open("test_report.html", "r", encoding='utf-8') as f:
            profile_html = f.read()

            # Add a wrapper div with full width and height to ensure the content fills the page
            full_page_html = f"""
            <div style="width: 100%; height: 100%;">
                {profile_html}
            </div>
            """

            components.html(full_page_html, height=1200, scrolling=True)
    
    except TypeError as te:
        st.error(f"TypeError: {te}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
