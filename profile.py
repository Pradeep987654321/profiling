import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
import tempfile

# Streamlit file uploader
st.title("CSV File Uploader and EDA Report")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding="latin-1")
        
        # Generate the profiling report
        profile = ProfileReport(df, minimal=True)

        # Create a temporary file to save the profiling report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            profile.to_file(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Load and display the HTML file
        with open(tmp_file_path, "r", encoding='utf-8') as f:
            profile_html = f.read()
            components.html(profile_html, height=1000, scrolling=True)
        
        # Provide a download link for the HTML file
        with open(tmp_file_path, "r", encoding='utf-8') as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="profile_report.html",
                mime="text/html"
            )
    
    except TypeError as te:
        st.error(f"TypeError: {te}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
