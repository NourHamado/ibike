import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_7():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'><b>Check-in: iBike Lesson Part 1</b></p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Check all descriptions that are correct about “manufacturing”</p>
        """,
        unsafe_allow_html=True
    )
    text_statements1 = [
        "The word manufacturing means made by machine.",
        "The manufacturing process is technological.",
        "The manufacturing process is economical.",
        "Manufacturing industry produces goods with added value.",
        "Manufacturing creates job opportunities."
    ]
    # styling text statements
    css_style = f"font-size: 20px;"

    selected_options1 = []  # a list to store selected options for text_statements1

    for statement in text_statements1:
        st.markdown(f'<div style="{css_style}">{statement}</div>', unsafe_allow_html=True)
        selected_option23 = st.radio("", ["Correct", "Incorrect"], index=0, key=statement)
        selected_options1.append(selected_option23)  # Store the selected option in the list

    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following statements is NOT true regarding manufacturing pillars?</p>
        """,
        unsafe_allow_html=True
    )
    statements07 = [
        "Manufacturing pillars are specific domains of knowledge necessary for bringing a concept of a product to the end user in the market.",
        "Business processes are distinct and separate from manufacturing.",
        "Manufacturing pillars benefit the economy by adding value to materials.",
        "Consumer's needs are an important part of the manufacturing pillars."
    ]
    selected_option45 = st.radio("", statements07)
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Product characteristics are defined during:
    </p>
        """,
        unsafe_allow_html=True
    )
    options05 = [
        "Product Design",
        "Concept Generation",
        "Prototyping",
        "Product Launch"
    ]
    selected_option56 = st.radio("", options05)
    st.markdown("---")

    selected_options34 = {}  # Initialize the dictionary here

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>In the product development cycle, which of the following stages fall under Concept Development? Select all that apply.
    </p>
        """,
        unsafe_allow_html=True
    )
    statements00 = [
        ("Abide by product specifications", "statement1"),
        ("Select the materials to produce it", "statement2"),
        ("Select the method to produce it", "statement3"),
        ("Launch the product to the market", "statement4")
    ]

    css_style = f"font-size: 20px;"

    for statement, key in statements00:
        st.markdown(f'<div style="{css_style}">{statement}:</div>', unsafe_allow_html=True)
        selected_options34[key] = st.radio("", ["Apply", "Do NOT apply"], key=key)
        st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Why is understanding the dynamic behavior of bikes important?
    </p>
        """,
        unsafe_allow_html=True
    )
    options098 = [
        "To better understand the stability of a bike",
        "To design an effective controller in case of electric bikes",
        "To be able to improve the design of a bike prior to construction"
    ]
    selected_option49 = st.radio("", options098)

    submit_button = st.button("Submit")

    if submit_button:
        if not all(selected_options1) or not selected_option45 or not selected_option56 or not all(selected_options34.values()) or not selected_option49:
            st.warning("Please fill all the required forms.")
        else:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
            gc = gspread.authorize(credentials)
            spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"
            sheet = gc.open_by_key(spreadsheet_id)
            worksheet_title = "Sheet5"
            worksheet = sheet.worksheet(worksheet_title)

            # Prepare the data for insertion as a list of lists
            data_to_insert = []
            data_to_insert.extend(selected_options1)
            data_to_insert.append(selected_option45)
            data_to_insert.append(selected_option56)
            data_to_insert.extend(list(selected_options34.values()))
            data_to_insert.append(selected_option49)

            # Insert the data into the worksheet without wrapping it in an additional list
            worksheet.insert_rows([data_to_insert], len(worksheet.get_all_values()) + 1)
            st.success("ibike Part1 Form has been successfully submitted.")
            return True
