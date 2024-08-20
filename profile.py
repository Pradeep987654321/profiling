import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport

# Apply custom CSS to remove padding and margins
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

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

        # Generate the profiling report
        profile = ProfileReport(df, title="Profiling Report")

        # Generate the HTML report as a string
        profile_html = profile.to_html()

        # Display the HTML report using st.markdown()
        st.markdown(profile_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
