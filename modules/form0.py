import streamlit as st
from streamlit import session_state as ss

def form_0():
	st.button("Back", on_click=toggle_survey_state)
	st.markdown(
		"""
		<p style='font-size: 20px; margin-bottom: 0;'>Do you want to take the survey? If you want to take please proceed.</p>
		""",
		unsafe_allow_html=True
	)
		#ss.survey_active = False;

def toggle_survey_state():
	if 'survey_active' not in ss:
		ss.survey_active = False;

	ss.survey_active = not(ss.survey_active)
