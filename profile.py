import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# Streamlit file uploader
st.title("CSV File Uploader and EDA Report")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, encoding="latin-1")
        

        # Generate and save the profiling report
        profile = ProfileReport(df, minimal=True)
        profile.to_file("test_report.html")
        st_profile_report(profile)


    
    except TypeError as te:
        st.error(f"TypeError: {te}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")




