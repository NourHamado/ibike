import streamlit as st
from streamlit import session_state as ss

def form_13():
    st.markdown(
            """
            <p style='font-size: 20px; margin-bottom: 0;'>Thank you for participating in survey.</p>
            """,
            unsafe_allow_html=True    
        )
    st.button("Finish Survey", on_click=toggle_survey_state)
        #ss.survey_active = False;

def toggle_survey_state():
	if 'survey_active' not in ss:
		ss.survey_active = False;

	ss.survey_active = not(ss.survey_active)
