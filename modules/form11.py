import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_11():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)

    st.markdown(
        """
        <p style='font-size: 24px; margin-bottom: 0;'><b>Check-in: iBike Lesson Part 3</b></p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Manufacturing paradigms are:</p>
        """,
        unsafe_allow_html=True
    )
    options_q5 = [
        "Production Volume", 
        "Manufacturing equipment", 
        "Manufacturing technologies", 
        "Manufacturing models that characterize a specific period", 
        "Manufacturing methods"
    ]

    selected_option_q5 = st.radio("", options_q5)
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>The evolution of the manufacturing paradigms is illustrated in the figure below using a volume-variety relationship. Match the letters in the second column to the manufacturing paradigm first column of the table below</p>
        """,
        unsafe_allow_html=True
    )
    st.image('files/images/ibike.jpg')
    title_manufacturing = ["Lean manufacturing", "Craft production", "Personalized production", "Mass customization", "Mass production"]
    css_style = f"font-size: 20px;"
    selected_choices1001 = []
    for title in title_manufacturing:
        st.markdown(f'<div style="{css_style}">{title}</div>', unsafe_allow_html=True)
        selected_choice1001 = st.radio("", ["A", "B/C", "D", "F", "Not Applicable"], index=0, key=title)
        selected_choices1001.append(selected_choice1001)
    st.markdown("---")   
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following did NOT drive manufacturing technology revolutions? </p>
        """,
        unsafe_allow_html=True
    )
    options_q1 = ["Steam", "Mechanical assembly", "Electricity", "Internet"]
    selected_option_q1 = st.radio("", options_q1)

    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following supply chain activities may impact a product’s final cost?</p>
        """,
        unsafe_allow_html=True
    )

    options_q2 = [
        "Purchasing raw materials from suppliers",
        "Transporting raw materials to manufacturing plants",
        "Manufacturing products",
        "Transporting products to distribution centers",
        "All of the above"
    ]

    selected_option_q2 = st.radio("", options_q2)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following statements about business processes is true?</p>
        """,
        unsafe_allow_html=True
    )

    options_q3 = [
        "They are executed across multiple functions.",
        "They are initiated by some type of trigger.",
        "They involve multiple activities.",
        "All of the above",
        "None of the above"
    ]

    selected_option_q3 = st.radio("", options_q3)

    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>The tendency of individuals to solely focus on the performance of their own activity with no concern or knowledge of the other tasks associated with proceeding or subsequent activities is called</p>
        """,
        unsafe_allow_html=True
    )

    options_q4 = [
        "The bottleneck effect",
        "The silo effect",
        "The blinders effect",
        "The manufacturing crossover"
    ]

    selected_option_q4 = st.radio("", options_q4)
    
    submit_button = st.button("Submit")

    if submit_button:
        data_to_insert = [selected_option_q5] + selected_choices1001 + [selected_option_q1, selected_option_q2, selected_option_q3, selected_option_q4]

        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        gc = gspread.authorize(credentials)
        spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet_title = "Sheet7"
        worksheet = sheet.worksheet(worksheet_title)

        worksheet.insert_rows([data_to_insert], len(worksheet.get_all_values()) + 1)
        st.success("iBike Part3 Form has been successfully submitted.")
        return True
