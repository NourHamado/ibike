import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_9():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)

    st.markdown(
        """
        <p style='font-size: 24px; margin-bottom: 0;'><b>Check-in: iBike Lesson Part 2</b></p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 1;'>The material used to make a product is limited by (select all that apply):</p>
        """,
        unsafe_allow_html=True
    )
    text_statements1010 = [
        "Its availability",
        "Its transportability",
        "Its affordability",
        "Its processibility",
        "Its processibility to meet specification."
    ]
    # styling text statements
    css_style = f"font-size: 20px;"
    selected_options1010 = []
    for statement in text_statements1010:
        st.markdown(f'<div style="{css_style}">{statement}</div>', unsafe_allow_html=True)
        selected_option1010 = st.radio("", ["Applies", "Does NOT Apply"], index=0, key=statement)
        selected_options1010.append(selected_option1010)
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom:1;'>Why do natural materials need to be processed? Select all that apply.</p>
        """,
        unsafe_allow_html=True
    )

    text_statements1011 = [
        "So that material's shape can change as needed by the product",
        "So that the material is more sanitary",
        "So that the material's properties can function the way desired by the product",
        "So that varied materials can be used and assembled into one product"
    ]
    # styling text statements
    css_style = f"font-size: 20px;"
    selected_options1011 = []
    for statement in text_statements1011:
        st.markdown(f'<div style="{css_style}">{statement}</div>', unsafe_allow_html=True)
        selected_option1011 = st.radio("", ["Applies", "Does NOT Apply"], index=0, key=statement)
        selected_options1011.append(selected_option1011)
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 1;'>What should be considered in selecting the method to process materials? Select all that apply.</p>
        """,
        unsafe_allow_html=True
    )
    text_statements1012 = [
        "The specifications of the product design",
        "Whether the method has the capacity to process materials demanded by the market",
        "Whether the method produces too much material waste",
        "Whether the processing method requires more investment in tools, space, etc."
    ]
    # styling text statements
    css_style = f"font-size: 20px;"
    selected_options1012 = []
    for statement in text_statements1012:
        st.markdown(f'<div style="{css_style}">{statement}</div>', unsafe_allow_html=True)
        selected_option1012 = st.radio("", ["Applies", "Does NOT Apply"], index=0, key=statement)
        selected_options1012.append(selected_option1012)
    
    submit_button = st.button("Submit")

    if submit_button:
        data_to_insert = selected_options1010 + selected_options1011 + selected_options1012

        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        gc = gspread.authorize(credentials)
        spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet_title = "Sheet6"
        worksheet = sheet.worksheet(worksheet_title)

        worksheet.insert_rows([data_to_insert], len(worksheet.get_all_values()) + 1)
        st.success("ibike Part2 Form has been successfully submitted.")
        return True
