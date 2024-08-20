import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from io import BytesIO

# Streamlit file uploader
st.title("CSV File Uploader and EDA Report")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding="latin-1")
        
        # Generate the profiling report
        profile = ProfileReport(df, minimal=True)
        
        # Save the profiling report to a BytesIO object
        with BytesIO() as buffer:
            profile.to_file(buffer)
            buffer.seek(0)
            
            # Provide a download link for the HTML file
            st.download_button(
                label="Download Report",
                data=buffer,
                file_name="profile_report.html",
                mime="text/html"
            )
    
    except TypeError as te:
        st.error(f"TypeError: {te}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
