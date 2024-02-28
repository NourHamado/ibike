import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_6():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)
    
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please indicate your level of agreement with the following statements. </p>
        """,
        unsafe_allow_html=True
    )
    
    text_titles1 = [
        "My parents see me as an engineer.",
        "My instructors see me as an engineer.",
        "My peers see me as an engineer.",
        "I am interested in learning more about engineering.",
        "I enjoy learning engineering.",
        "I find fulfillment in doing engineering.",
        "I am confident that I can understand engineering in class.",
        "I am confident that I can understand engineering outside of class.",
        "I can do well on exams in engineering.",
        "I understand concepts I have studied in engineering.",
        "Others ask me for help in this subject."
    ]
    
    css_style = f"font-size: 20px;"
    
    selected_options1 = []  # a list to store selected options for text_titles1
    
    for title in text_titles1:
        st.markdown(f'<div style="{css_style}">{title}:</div>', unsafe_allow_html=True)
        selected_option08 = st.radio("", ["Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree"], index=3, key=title)
        selected_options1.append(selected_option08)  # Store the selected option in the list
    
    st.markdown("---")
    
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 1;'>Please indicate your level of agreement with the following statements. </p>
        """,
        unsafe_allow_html=True
    )
    
    text_titles2 = [
        "I can master the content in the engineering-related courses I am taking this semester.",
        "I can master the content in even the most challenging engineering course.",
        "I can do a good job on almost all my engineering coursework.",
        "I can learn the content taught in my engineering-related courses.",
        "I can earn a good grade in my engineering-related courses."
    ]
    
    selected_options2 = []  # a list to store selected options for text_titles2
    
    for title in text_titles2:
        st.markdown(f'<div style="{css_style}">{title}:</div>', unsafe_allow_html=True)
        selected_option09 = st.radio("", ["Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree"], index=3, key=title)
        selected_options2.append(selected_option09)  # Store the selected option in the list
    
    submit_button = st.button("Submit")
    
    if submit_button:
        if not all(selected_options1) or not all(selected_options2):
            st.warning("Please fill all the required forms.")
        else:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
            gc = gspread.authorize(credentials)
            spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"
            sheet = gc.open_by_key(spreadsheet_id)
            worksheet_title = "Sheet4"
            worksheet = sheet.worksheet(worksheet_title)
            
            # Prepare the data for insertion as a list of lists
            data_to_insert = []
            data_to_insert.extend(selected_options1)
            data_to_insert.extend(selected_options2)
            
            # Insert the data into the worksheet without wrapping it in an additional list
            worksheet.insert_rows([data_to_insert], len(worksheet.get_all_values()) + 1)
            st.success("Level Of Agreement Form has been successfully submitted.")
            return True
