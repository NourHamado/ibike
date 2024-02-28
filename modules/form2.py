import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_2():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)
    
    javascript_code = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
    const textArea = document.querySelector('textarea');
    textArea.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        }
    });
    });
    </script>
    """
    
    selected_age, selected_option_q40, other_input_gender, selected_option_q41, other_input_race, selected_gpa, selected_option, other_input_college, input_major = "", "", "", "", "", "", "", "", ""
    
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please select your age.</p>
        """,
        unsafe_allow_html=True
    )
    selected_age = st.selectbox("", list(range(18, 61)))
    
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please select your gender</p>
        """,
        unsafe_allow_html=True
    )
    options_q40 = [
        "Male", 
        "Female", 
        "Transgender female", 
        "Transgender male",
        "Non-binary/third gender",
        "Prefer not to say",
        "Not Listed"
    ]
    selected_option_q40 = st.radio("", options_q40)
    
    other_input_gender = ""
    if selected_option_q40 == "Not Listed":
        other_input_gender = st.text_input("Please specify your gender", key="text_input_gender")

    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please select your race:</p>
        """,
        unsafe_allow_html=True
    )
    options_q41 = [
        "Asian or Pacific Islander", 
        "Black or African American", 
        "Hispanic or Latino", 
        "Native American or Alaskan native", 
        "White or Caucasian", 
        "Multiracial or Biracial", 
        "Prefer not to say",
        "A Race/ethnicity not listed here"
    ]
    selected_option_q41 = st.radio("", options_q41)
    
    other_input_race = ""
    if selected_option_q41 == "A Race/ethnicity not listed here":
        other_input_race = st.text_input("Please specify your race/ethnicity", key="text_input_race")
    
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin: 0;'>What is your cumulative GPA?</p>""",
        unsafe_allow_html=True
    )
    selected_gpa = st.selectbox("", [str(x/10) for x in range(40, 19, -1)])
    
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What year of college are you in?.</p>
        """,
        unsafe_allow_html=True
    )
    selected_option = st.radio("", ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Not Listed"], key="selected_option34")
    
    other_input_college = ""
    if selected_option == "Not Listed":
        other_input_college = st.text_input("Please specify your college year", key="text_input_college")
    
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is your major?</p>
        """,
        unsafe_allow_html=True
    )
    input_major = st.text_input("Please specify your engineering major:", key="text_input_major")
    
    submit_button = st.button("Submit")
    required_fields_empty = False

    if selected_option_q40 == "Not Listed" and not other_input_gender:
        required_fields_empty = True

    if selected_option_q41 == "A Race/ethnicity not listed here" and not other_input_race:
        required_fields_empty = True

    if selected_option == "Not Listed" and not other_input_college:
        required_fields_empty = True

    if not input_major:
        required_fields_empty = True

    if required_fields_empty and submit_button:
        st.warning("Please fill in all the required fields.")
    elif submit_button:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        gc = gspread.authorize(credentials)
        #gsspreadsheet where data will be stored
        spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"  # Replace with your Spreadsheet ID
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet_title = "Sheet2"
        worksheet = sheet.worksheet(worksheet_title)
        
        form_data1 = {
            'Age': selected_age,
            'Gender': selected_option_q40,
            'Other Gender': other_input_gender,
            'Race': selected_option_q41,
            'Other Race': other_input_race,
            'GPA': selected_gpa,
            'College Year': selected_option,
            'Other College Year': other_input_college,
            'Major': input_major
        }
            
        num_rows = len(worksheet.get_all_values())
        worksheet.insert_rows([list(form_data1.values())], num_rows+1)
        st.success("Basic Information Form has been successfully submitted")
        return True
