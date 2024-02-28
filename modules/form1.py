import streamlit as st
from streamlit import session_state as ss
import json
from datetime import date
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_1():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)
    first_name, last_name, selected_date, option_1, option_2, option_3, option_4, option_5, option_6, option_7, option_8, option_9, other_input = "", "", date(2023, 10, 1), False, False, False, False, False, False, False, False, False, ""
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
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.write("Dear students,")
    st.markdown("""The School of Engineering is conducting an educational research study on the impact of a curriculum that integrates business with industrial knowledge and engineering (iBIKE) to improve manufacturing education (NSF funding pending). 
                 The curriculum is consisted of several modules that will be implemented in the following courses: IE 305, EE380, EE383 (lab), ME 465 (lab), ME 468, ME 469, IE 470, and MIS 404. 
                 All students enrolled in these courses are invited to participate in the study.__The purpose of the study__ is to transform manufacturing education and develop associated skills by integrating manufacturing concepts across engineering.
                 The curriculum modules will be designed and improved based on student feedback over a period of three years.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Procedure__: This study will not change or add class meeting time if you are enrolled in the above listed courses. 
                 However, students will be asked to fill out a couple of short surveys before and after selected classes. 
                 Only the information of consented participants will be included in the study’s database. 
                 The information will be deidentified prior to analysis. Data will be analyzed as a group and may be used in an academic presentation or journal publication. 
                 However, no personally identifiable information will be used or shared.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Statement of Confidentiality__: Only researcher(s) has the knowledge of participant names. Your course instructor will not have such knowledge. 
                 Digital data will be stored and secured in a locked file cabinet and password-protected computer behind uofl firewall and two-factor authentication. 
                 The collected data will be compiled by researcher to data analysis. 
                 In the event of a publication or presentation resulting from the research, no personally identifiable information will be included.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Discomforts and Risks:__ Though a participant might feel some discomfort knowing that his/her grades and comments are being viewed, we would like to assure the participants that all information will be confidential and no names or individual demographic information will appear in any written analysis of the data.
                 There are no risks in participating in this research beyond those experienced in everyday life.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Compensation__:  There will be no compensation for participation in this research.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Benefits__: We hope the integrated curriculum will bring improved learning experiences for students.
                 As educators, we hope to create high quality curriculum and better prepare engineering students for the real world.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Duration/time__: The study will last three years, and each course takes one semester, some con-currently. The short surveys will likely be filled in regular class time. Participants will not need to meet outside of class for the research.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""Right to Ask Questions: Please contact Dr. Aqlan if you have questions or concerns about this research.  You can also inquire him through email if you feel this study has harmed you. If you have questions about your rights as a research participant, contact university of Louisville.""")
    st.markdown("")
    st.markdown("")
    st.markdown("""__Voluntary Participation__:  Your decision on whether to have your data included in this research is voluntary.  You can withdraw at any time.  You do not have to answer any survey questions if you do not feel comfortable answering. 
                 Participation or non-participation in the study will have no effect on grades or status with your instructor or the university.""")
    st.markdown("")
    st.markdown("You must be 18 years of age or older to consent to take part in this research study.")
    st.markdown("")
    st.markdown("By typing your name below and submitting this form, you agree to take part in this research study and the information outlined above.")
    st.markdown("")
    # #hyperlink
    # css = """
    # <style>
    # /* Style the hyperlink text */
    # .custom-link {
    #     font-size: 20px;
    #     color: blue; /* Link color */
    # }
    # </style>
    # """
    # st.markdown(css, unsafe_allow_html=True)
    # st.markdown('<a class="custom-link" href="https://louisville.app.box.com/s/rjhk2aak9dt4f3hoehydjci6zqx34qt9" target="_blank">Consent form iBike</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Consent for participation.</p>
        """,
        unsafe_allow_html=True
    )
    selected_option100 = st.radio("",["I consent to participate in the above described research study.", "I DO NOT consent to participate in the above described research study."], key="consent_form_radio")
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please enter your name:</p>
        """,
        unsafe_allow_html=True
    )
    first_name = st.text_input('First Name', '')
    last_name = st.text_input('Last Name', '')
    st.markdown("---")
    st.markdown(
        """
        <style>
        .title-text {
            font-weight: normal;
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Please enter today's date:</p>
        """,
        unsafe_allow_html=True
    )
    selected_date = st.date_input("", date(2023, 10, 1))
    date_string = selected_date.strftime("%Y-%m-d")
    st.markdown("___")
    st.markdown("<span style='font-size:20px;'>Which class are you currently enrolled in that shared this survey with you?</span>", unsafe_allow_html=True)
        
    option_1 = st.checkbox('IE 305')
    option_2 = st.checkbox('EE 380')
    option_3 = st.checkbox('EE 383 (lab)')
    option_4 = st.checkbox('ME 468')
    option_5 = st.checkbox('ME 469')
    option_6 = st.checkbox('ME 465 (lab)')
    option_7 = st.checkbox('IE 470')
    option_8 = st.checkbox('MIS 404')
    option_9 = st.checkbox('Other')
        
    if option_9:
        other_input = st.text_input("Please specify the other class", key="text_input_76")            
    else:
        other_input = ""
                
    submit_button = st.button("Submit")
    if submit_button:
        warnings = []
        if not first_name or not last_name or not (option_1 or option_2 or option_3 or option_4 or option_5 or option_6 or option_7 or option_8 or (option_9 and other_input)):
            warnings.append("Please fill all the required forms.")

        if warnings:
            st.warning("\n".join(warnings))
        else:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
            gc = gspread.authorize(credentials)
            #gsspreadsheet where data will be stored
            spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"  # Replace with your Spreadsheet ID
            sheet = gc.open_by_key(spreadsheet_id)
            worksheet_title = "Sheet1"
            worksheet = sheet.worksheet(worksheet_title)
            #dictionary to hold the form data
            form_data = {
                'Consent': selected_option100,
                'First Name': first_name,
                'Last Name': last_name,
                'Date': date_string,
                'IE 305': option_1,
                'EE 380': option_2,
                'EE 383 (lab)': option_3,
                'ME 468': option_4,
                'ME 469': option_5,
                'ME 465 (lab)': option_6,
                'IE 470': option_7,
                'MIS 404': option_8,
                'Other': other_input
            }
            num_rows = len(worksheet.get_all_values())
            worksheet.insert_rows([list(form_data.values())], num_rows+1)
            st.success(f"Consent submitted with name: {first_name} {last_name}")
            return True
