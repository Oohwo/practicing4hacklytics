import streamlit as st
import pandas as pd

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title("Job Postings App!")
st.divider()
st.markdown("Practicing Streamlit with a [Kaggle dataset about job postings](https://www.kaggle.com/datasets/moyukhbiswas/job-postings-dataset) for the upcoming Hacklytics competition.")
st.markdown("Please ignore whatever's in the sidebar! Those other pages came along with the codespace :^)")
st.divider()

st.markdown("## View Dataset")
# extract the data
def extract_data():
  df = pd.read_csv("job_postings.csv")
  return df

# fill missing data
def data_manipulation(df):
  df = df.drop("Unnamed: 0", axis=1) # drop this col
  df.columns = df.columns.str.lower() # lowercase the columns
  df = df.fillna("unspecified") # replace blanks w unspecified 
  return df

# see this: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def filter_df(df: pd.DataFrame) -> pd.DataFrame:
  modify = st.checkbox("Add filters")

  if not modify:
    return df
  
  modification_container = st.container()

  with modification_container:
    to_filter_columns = st.multiselect("Filter data...", df.columns)

    for column in to_filter_columns:
      left, right = st.columns((1, 20))
      left.write("↳")

      if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
        user_cat_input = right.multiselect(
          f"Select values for `{column}`:",
          df[column].unique(),
          default=list(df[column].unique())
        )
        df = df[df[column].isin(user_cat_input)]
      else:
        user_text_input = right.text_input(
          f"Start typing the `{column} (case-sensitive):"
        )

        if user_text_input:
          df = df[df[column].str.contains(user_text_input)]
    
    return df

with st.spinner("Extracting Data..."):
  df = extract_data()
  df = data_manipulation(df)

st.dataframe(filter_df(df))
st.markdown(f"The original dataset contains {df.shape[0]} rows and {df.shape[1]} columns!")

st.markdown("## Visualizations")