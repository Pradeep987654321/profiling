import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
import tempfile
import base64
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
# Apply custom CSS to remove padding and margins and position buttons at the bottom
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
        z-index: 1;
    }
    .button-container {
        position: fixed;
        bottom: 10px;
        right: 10px;
        z-index: 1000;
    }
    .button-container a {
        text-decoration: none;
        margin: 0 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit file uploader
st.title("CSV File Uploader and EDA Report")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner('Generating report...'):
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file, encoding="latin-1")
            
            # Generate the full profiling report
            profile = ProfileReport(df)

            # Create temporary files for HTML and JSON reports
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as html_file:
                profile.to_file(html_file.name)
                html_file_path = html_file.name

            # Save JSON manually
            json_report = profile.to_json()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as json_file:
                json_file.write(json_report.encode('utf-8'))
                json_file_path = json_file.name

            # Provide download buttons for HTML and JSON files
            def get_base64_file(file_path):
                with open(file_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()

            st.markdown(
                f"""
                <div class="button-container">
                    <a href="data:file/html;base64,{get_base64_file(html_file_path)}" download="profile_report.html">
                        <button>Download HTML Report</button>
                    </a>
                    <a href="data:file/json;base64,{get_base64_file(json_file_path)}" download="profile_report.json">
                        <button>Download JSON Report</button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Load and display the HTML file
            with open(html_file_path, "r", encoding='utf-8') as f:
                profile_html = f.read()

                # Add a wrapper div with full width and height to ensure the content fills the page
                full_page_html = f"""
                <div style="width: 100%; height: 100%; position: relative;">
                    {profile_html}
                </div>
                """

                components.html(full_page_html, height=1200, scrolling=True)
        
        except TypeError as te:
            st.error(f"TypeError: {te}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
