import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def form_12():
    json_file_path = "./modules/my-credentials.json"
    with open(json_file_path, 'r') as file_obj:
        credentials = json.load(file_obj)

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is manufacturing?</p>
        """,
        unsafe_allow_html=True
    )
    options_q30 = [
        "A process that attempts to decompose an object into its basic units.", 
        "A process that transforms raw materials into finished products to add value.", 
        "A process that supports delivery or maintenance of tangible commodities.", 
        "A process that measures operational reliability and assures conformance to specifications."
    ]
    selected_option_q30 = st.radio("", options_q30)
    st.markdown("---")
    
    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following is NOT a component of manufacturing?</p>
        """,
        unsafe_allow_html=True
    )
    options_q31 = [
        "Adds value", 
        "Transforms raw materials", 
        "Creates products", 
        "Extracts material"
    ]
    selected_option_q31 = st.radio("", options_q31)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What are the six pillars of manufacturing?</p>
        """,
        unsafe_allow_html=True
    )
    options_q32 = [
        "1. Requirements Analysis, 2. Product Design, 3. Processes Configuration, 4. Production Planning, 5. Product Assembly, 6. Product Delivery", 
        "1. Product Design, 2. Manufacturing Materials, 3. Manufacturing Processes, 4. Manufacturing Systems, 5. Manufacturing Technologies, 6. Business Processes.", 
        "1. Conceptualization, 2. Resource planning, 3. Resource Scheduling, 4. Task assignment, 5. Execution, 6. Termination", 
        "1. Analyzing, 2. Designing, 3. Manufacturing, 4. Testing, 5. Delivering, and 6. Maintaining"
    ]
    selected_option_q32 = st.radio("", options_q32)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following is NOT a characteristic of a pillar of manufacturing?</p>
        """,
        unsafe_allow_html=True
    )
    options_q33 = [
        "Provides knowledge in a defined manufacturing area.", 
        "A building block of manufacturing that is characterized by a specific domain knowledge in manufacturing.", 
        "Includes product design, manufacturing materials, manufacturing processes, manufacturing systems, manufacturing technologies, and business processes.", 
        "Decomposition of an object into its basic units."
    ]
    selected_option_q33 = st.radio("", options_q33)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is the definition of Product Design?</p>
        """,
        unsafe_allow_html=True
    )
    options_q34 = [
        "The process of making the product and delivering it to the end customer.", 
        "The process of importing the raw material from the supplier.", 
        "The process of defining product characteristics (e.g., dimensions, appearance, materials, tolerance, etc.)", 
        "The process of transforming the raw material into the finished product."
    ]
    selected_option_q34 = st.radio("", options_q34)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is the definition of Manufacturing Materials?</p>
        """,
        unsafe_allow_html=True
    )
    options_q35 = [
        "The input materials or substances used in the production of goods.", 
        "The input material which is disposed of after production.", 
        "The input material which assists the production but is not a part of the final product.", 
        "The input material which is dissipated during production."
    ]
    selected_option_q35 = st.radio("", options_q35)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is the definition of Manufacturing Processes?</p>
        """,
        unsafe_allow_html=True
    )
    options_q36 = [
        "A sequence of steps to decide the manufacturing process", 
        "A sequence of steps to design the product.", 
        "A sequence of steps to decide the cost of the product.", 
        "A specified combination or sequence of steps through which raw material is transformed into a final product."
    ]
    selected_option_q36 = st.radio("", options_q36)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is the definition of Business Processes?</p>
        """,
        unsafe_allow_html=True
    )
    options_q37 = [
        "A sequence of related tasks designed for some type of financial gain.", 
        "A series of tasks associated with generating revenue or incurring costs.", 
        "A collection of tasks related to the oversight and management of people within the organization.", 
        "A collection of linked tasks which support the receipt, execution, and/or delivery of a service or product."
    ]
    selected_option_q37 = st.radio("", options_q37)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>Which of the following statements BEST describes the product development life cycle?</p>
        """,
        unsafe_allow_html=True
    )
    options_q38 = [
        "Progression of phases that follow a product over time from creation to maturity and finally to decline.", 
        "The sequence of stages necessary to take a product from an idea to the end customer.", 
        "The progression of a product through a series of stages from design to manufacturing.", 
        "The sequence of stages that a product goes through from its manufacturing to its delivery to the end customer."
    ]
    selected_option_q38 = st.radio("", options_q38)
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size: 20px; margin-bottom: 0;'>What is the correct order of the stages of the product development lifecycle?</p>
        """,
        unsafe_allow_html=True
    )
    options_q39 = [
        "1. Concept, 2. Launch, 3. Development, 4. Manufacture, 5. Test, 6. Sell", 
        "1. Product Design, 2. Manufacturing Materials, 3. Manufacturing Processes, 4. Manufacturing Systems, 5. Manufacturing Technologies, 6. Business Processes.", 
        "1. Concept, 2. Design, 3. Plan, 4. Manufacture, 5. Test, 6. Store", 
        "1. Concept, 2. Development, 3. Prototype, 4. Manufacture, 5. Launch, 6. Distribution"
    ]
    selected_option_q39 = st.radio("", options_q39)

    submit_button = st.button("Submit")

    if submit_button:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        gc = gspread.authorize(credentials)
        spreadsheet_id = "1UiBuyoFudQnvgzgIxlh__6ktEBKK7zJvqoWYwz_2WuE"  # Replace with your Spreadsheet ID
        sheet = gc.open_by_key(spreadsheet_id)
        worksheet_title = "Sheet8"
        worksheet = sheet.worksheet(worksheet_title)
        data_to_insert = [
            selected_option_q30, selected_option_q31, selected_option_q32, selected_option_q33, 
            selected_option_q34, selected_option_q35, selected_option_q36, selected_option_q37, 
            selected_option_q38, selected_option_q39
        ]
        worksheet.insert_rows([data_to_insert], len(worksheet.get_all_values()) + 1)
        st.success("Manufacturing Form has been successfully submitted.")
        return True
