import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_4():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)

    user_input1 = st.text_area("In your own words, define manufacturing:")
    user_input2 = st.text_area("In your own words, define manufacturing pillars:")
    user_input3 = st.text_area("List and briefly describe the six pillars:")
    user_input4 = st.text_area("In your own words, define manufacturing systems:")
    user_input5 = st.text_area("In your own words, define manufacturing technologies?")
    user_input6 = st.text_area("In your own words, define product development lifecycle:")

    submit_button = st.button("Submit")

    if submit_button:
        if not user_input1 or not user_input2 or not user_input3 or not user_input4 or not user_input5 or not user_input6:
            st.warning("Please fill all the required forms.")
        else:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
            gc = gspread.authorize(credentials)

            # Google Spreadsheet where data will be stored
            spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"  # Replace with your Spreadsheet ID
            sheet = gc.open_by_key(spreadsheet_id)
            worksheet_title = "Sheet3"
            worksheet = sheet.worksheet(worksheet_title)

            form_data = {
                'In your own words, define manufacturing.': user_input1,
                'In your own words, define manufacturing pillars.': user_input2,
                'List and briefly describe the six pillars.': user_input3,
                'In your own words, define manufacturing systems.': user_input4,
                'In your own words, define manufacturing technologies?': user_input5,
                'In your own words, define product development lifecycle?': user_input6
            }

            num_rows = len(worksheet.get_all_values())
            worksheet.insert_rows([list(form_data.values())], num_rows + 1)
            st.success("Defining Manufacturing Terms Form has been successfully submitted.")
            return True
