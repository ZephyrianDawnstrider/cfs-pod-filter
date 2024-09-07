import streamlit as st
import pandas as pd

def handle_uploaded_file(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return {}

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return {}

    df.columns = df.columns.str.strip().str.upper()
    pod_column = 'POD'
    cfs_column = 'CFS'
    
    filtered_df = df[df[pod_column].str.upper().str.contains('PPG', na=False)]

    try:
        unique_cfs_names = filtered_df[cfs_column].str.split(',').explode().str.strip().unique()
    except Exception as e:
        st.error(f"Error processing 'CFS' column: {e}")
        return {}

    output_files = {}

    for name in unique_cfs_names:
        try:
            name_filtered_df = filtered_df[filtered_df[cfs_column].str.contains(name, na=False)]
            output_filename = f'filtered_data_{name.replace(" ", "_")}.csv'
            name_filtered_df.to_csv(output_filename, index=False)
            output_files[name] = output_filename
        except Exception as e:
            continue

    return output_files

st.title('Filter CFS and POD')

uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    filtered_files = handle_uploaded_file(uploaded_file)

    if filtered_files:
        st.write("Files ready for download:")
        for name, file in filtered_files.items():
            with open(file, 'rb') as f:
                st.download_button(
                    label=f"Download {name}",
                    data=f.read(),
                    file_name=file,
                    mime='text/csv'
                )
