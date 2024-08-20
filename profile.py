import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
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
        
        # Save the profiling report to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            profile.to_file(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Provide a download link for the HTML file
        with open(tmp_file_path, "rb") as f:
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
