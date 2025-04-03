#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper" , layout="wide")
st.title("Data Sweeper")
st.write("Transform your file between CVS and Excel formates with built_in data cleaning and visualization")

uploaded_file = st.file_uploader("Choose a file:", type=["csv", "xlsx"], accept_multiple_files=True)


if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.write("Invalid file format: {file_ext}")
            continue   

        
    st.write(f"**File Name:** {file.name}")
    st.write(f"**File Size:** {file.size/1024}")

    st.write("Preview the Head of the Dataframe")
    st.dataframe(df.head())

    st.subheader("Data Cleaning Options")
    if st.checkbox(f"Clean Data for {file.name}"):
        cols1 , cols2 = st.columns(2)
        with cols1:
            if st.button(f"Remove Duplicates from {file.name}"):
             df.drop_duplicates(inplace = True)
             st.write("Duplicates Removed!")
        with cols2:
             if st.button(f"Fill Null Values in {file.name}"):
                 numeric_cols = df.select_dtypes(include = ["number"]).columns
                 df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                 st.write("Null Values Filled!")


    st.subheader("Select the File Format to Save")
    columns = st.multiselect(f"Select Columns to Save in {file.name}", df.columns , default = df.columns)
    df = df[columns]


    st.subheader("Data  Visualization")
    if st.checkbox(f"Show Data Visualization for {file.name}"):
       st.bar_chart(df.select_dtypes(include = 'number').iloc[: ,:2])

    st.subheader("Conversion Options")
    conversion_format = st.radio(f"Select {file.name} to:", ["csv" , "xlsx"] , key = file.name)
    if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_format == "csv":
                df.to_csv(buffer , index = False)
                file_name = file.name.replace(file_ext , ".csv")
                mine_type = "text/csv"
            
            elif conversion_format == "Excel":
                df.to_excel(buffer , index = False)
                file_name = file.name.replace(file_ext , ".xlsx")
                mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)    


            st.download_button(
                label = f"download {file.name} to {conversion_format}",
                data = buffer,
                file_name = file_name,
                mime = mine_type

            )

            st.success(f"{file.name} has been converted to {conversion_format}")

            
        

        