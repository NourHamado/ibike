import streamlit as st
import numpy as np
import pandas as pd
from os import path
import os
import time
from streamlit import session_state as ss
from modules import order, group, player, game, player_rejoin
from enum import Enum
from shutil import make_archive
import decimal
import datetime

class ReportState(Enum):
	INACTIVE = 1
	CONFIRMING = 2
	GENERATING = 3
	FINISHED = 4
	INVALID = 5

def render():

	if 'code_written' not in ss:
		ss['code_written'] = False

	if not ss.code_written:
		display_pr_m_code()
	else:
		
		st.title('Project Manager')

		st.write("Welcome to the Project Manager Page!")
		
		st.markdown(
				"""
				Your role is to generate customer orders, monitor the progress of your team members, delegate tasks, and provide constructive feedback.
				""")
		if 'order_requested' not in ss:
			ss['orders_requested'] = False
		if 'display_orders' not in ss:
			ss['display_orders'] = False
		if 'orders_full' not in ss:
			ss['orders_full'] = False

		st.markdown("Specify the number of orders you would like to place using the slider, and then click \"Generate Customer Orders\".")

		col1, col2 = st.columns([1, 2])

		with col1:
			
			order_request = st.button('Generate Customer Orders',on_click=create_orders)
			
			if ss.orders_requested:
				st.write(f"{ss.orders_created} orders have been recieved. There are {len(ss.group_state['orders'])} ongoing orders. Click on 'View/Hide Orders' to see order details.")
				
			if ss.orders_full:
				st.write(f"WARNING: That number of incoming orders will exceed the current limit of {ss.order_limit} ongoing customer orders. Select a smaller number of orders.")
				
		with col2:
			
			num_requested = st.slider('Select the number of orders you would like to generate:', key="num_orders", min_value=1, max_value=ss.order_limit, value=1)

		st.markdown('---')
		ss.date = st.date_input("Choose the order complation date", value=None)
		
		st.markdown('---')
		player.display_current_orders()
		st.markdown('---')

		if 'report_status' not in ss:
				#ss.report_status = ReportState.INACTIVE
				ss.report_status = ReportState.GENERATING

		#this is checked up here so that clicking "Refresh" will immediately show if the report is ready
		if(ss.report_status == ReportState.GENERATING):
			check_report()
		
		st.write(f"As Project Manager, you can report your progress to the instructor by creating a downloadable report. You can download the report only once, so make sure to download it at the end of the simulation")
		st.write(f"NOTE: You will not be able to create the report until all the players submit their report information")
		#report button
		'''if(ss.report_status == ReportState.INACTIVE):
			st.button('Create Report', on_click=advance_state)
		elif(ss.report_status == ReportState.CONFIRMING):
			st.button('Cancel Report', on_click=reset_state)'''
		if(ss.report_status == ReportState.GENERATING):
			st.button('Create Report') #this button doesn't really do anything, but clicking it will cause the check_report to be run again
		elif (ss.report_status == ReportState.FINISHED):
			st.button('Close Report', on_click=advance_state)
		else:
			print('State Error - Button') #this should never be reached unless an error occurs

		#revealed items that appear once the button is clicked for the first time
		if(ss.report_status != ReportState.INACTIVE):
			if(ss.report_status == ReportState.CONFIRMING):
				st.write(f"Are you sure you want to make a report? You can continue playing, but your additional progress will not be reflected in the report.")
				st.button('Confirm', on_click=generate_report) #this function call will advance the report state
			elif(ss.report_status == ReportState.GENERATING):
				st.write(f" ")			
			elif(ss.report_status == ReportState.FINISHED):
				st.write(f"Report generated successfully. You may now close this report.")
			else:
				print('State Error - Revealed Area') #this also should never be reached unless an error occurs
		
		if path.isfile(ss.filepath+'parts_selction.csv'):
			st.header(":blue[Mechanical Engineer]")
			st.markdown("Parts, materials, and manufacturing processes selected by the :blue[Mechanical Engineer]")
			selection_df = pd.read_csv(ss.filepath+'parts_selction.csv')
			selection_df.index = list(range(1, len(selection_df)+1))
			st.dataframe(selection_df, width=3000)
		
		if path.isfile(ss.filepath+'parts_material_process_justification.csv'):
			st.markdown("Justifications of the :blue[Mechanical Engineer]")
			just_df = pd.read_csv(ss.filepath+'parts_material_process_justification.csv')
			just_df.index = list(range(1, len(just_df)+1))
			st.dataframe(just_df, width=3000)
		
	
def feedback():
	st.header("Feedback **:red[TO]**")
	
	text = ""
	if path.isfile(ss.filepath+'fb_pm_m.txt'):
		with open(ss.filepath+'fb_pm_m.txt', 'r') as f:
			text = f.read()

	with st.form("proj_mech_feedback"):
		fb_pm_m = st.text_area("Your feedback to the Mechanical Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pm_m != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_pm_m.txt", "w") as f:
					f.write(fb_pm_m)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun() #causes the submit button to only need to be pressed once
		elif (clear_submission):
			with st.spinner("Clearing feedback..."):
				time.sleep(1)
				if path.isfile(ss.filepath+'fb_pm_m.txt'):
					os.remove(ss.filepath+'fb_pm_m.txt')
					st.success("Feedback cleared!", icon="✅")
			st.experimental_rerun() #causes the submit button to only need to be pressed once
	
	if path.isfile(ss.filepath+'orders.csv'):
		st.header(":blue[Industrial Engineer]")
		st.markdown("Orders by the :blue[Industrial Engineer]")
		orders_df = pd.read_csv(ss.filepath+'orders.csv')
		orders_df.index = list(range(1, len(orders_df)+1))
		st.dataframe(orders_df, width=3000)
	
	text = ""
	if path.isfile(ss.filepath+'fb_pm_i.txt'):
		with open(ss.filepath+'fb_pm_i.txt', 'r') as f:
			text = f.read()

	with st.form("proj_ind_feedback"):
		fb_pm_i = st.text_area("Your feedback to the Industrial Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pm_i != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_pm_i.txt", "w") as f:
					f.write(fb_pm_i)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			with st.spinner("Clearing feedback..."):
				time.sleep(1)
				if path.isfile(ss.filepath+'fb_pm_i.txt'):
					os.remove(ss.filepath+'fb_pm_i.txt')
					st.success("Feedback cleared!", icon="✅")
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_pm_pum.txt'):
		with open(ss.filepath+'fb_pm_pum.txt', 'r') as f:
			text = f.read()

	with st.form("proj_pur_feedback"):
		fb_pm_pum = st.text_area("Your feedback to the Purchasing Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pm_pum != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_pm_pum.txt", "w") as f:
					f.write(fb_pm_pum)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			with st.spinner("Clearing feedback..."):
				time.sleep(1)
				if path.isfile(ss.filepath+'fb_pm_pum.txt'):
					os.remove(ss.filepath+'fb_pm_pum.txt')
					st.success("Feedback cleared!", icon="✅")
			st.experimental_rerun()
			
	text = ""
	if path.isfile(ss.filepath+'fb_pm_d.txt'):
		with open(ss.filepath+'fb_pm_d.txt', 'r') as f:
			text = f.read()

	with st.form("proj_des_feedback"):
		fb_pm_d = st.text_area("Your feedback to the Design Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pm_d != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_pm_d.txt", "w") as f:
					f.write(fb_pm_d)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			with st.spinner("Clearing feedback..."):
				time.sleep(1)
				if path.isfile(ss.filepath+'fb_pm_d.txt'):
					os.remove(ss.filepath+'fb_pm_d.txt')
					st.success("Feedback cleared!", icon="✅")
			st.experimental_rerun()
	
	# reading
	st.header("Feedback **:red[From]**")
	st.button('Click here to refresh the feedback from other players')
	st.markdown("---")
	if path.isfile(ss.filepath+'fb_d_pm.txt'):
		st.write("Feedback from the **:red[Design Engineer]**:")
		with open(ss.filepath+'fb_d_pm.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_i_pm.txt'):
		st.write("Feedback from the **:red[Industrial Engineer]**:")
		with open(ss.filepath+'fb_i_pm.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_m_pm.txt'):
		st.write("Feedback from the **:red[Mechanical Engineer]**:")
		with open(ss.filepath+'fb_m_pm.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_pum_pm.txt'):
		st.write("Feedback from the **:red[Purchasing Manager]**:")
		with open(ss.filepath+'fb_pum_pm.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

def create_orders():
		
	if len(ss.group_state['orders']) + ss.num_orders <= ss.order_limit:
		for i in range(ss.num_orders):
			group.add_new_order(ss.group)
		ss.orders_requested = True
		ss.orders_full = False
		ss['orders_created'] = ss.num_orders
	else:
		ss.orders_requested = False
		ss.orders_full = True
	
def switch_orders_display():
	if ss.display_orders == True:
		ss.display_orders = False
	else:
		ss.display_orders = True

def submit_order_info(order_key):
	group_state = group.load(ss.group)
	group_state['orders'][order_key]['order_completion_date'] = str(ss.date)
	group.save_group_state(group_state)

def advance_state():
	ss.report_status = ReportState(ss.report_status.value + 1)
	if (ss.report_status.value > 4):
		reset_state()

def reset_state():
	ss.report_status = ReportState(1)

def generate_report():
	group_state = group.load(ss.group_state.get('group_key'))
	#setting this boolean array to all false prompts the other roles to create heir files for the report
	for i in range(4):
		(group_state['roles_reported'])[i] = False
	group.save_group_state(group_state)
	
	advance_state()

def check_report():
	#all other roles must update their page in order to automatically submit the info for the report, so that is checked here
	group_state = group.load(ss.group_state.get('group_key'))
	submission_count = 0

	#checking how many players have submitted
	for i in range(4):
		if((group_state['roles_reported'])[i] == True):
			submission_count += 1
	if submission_count == 4:
		end_time = time.time()
	if(submission_count == group_state['player_count'] - 1):
		#resetting boolean array so that new players who join don't try to submit a report
		if(group_state['player_count'] < 4):
			for i in range(4):
				(group_state['roles_reported'])[i] = True

		#making the zip file and adding additional group info file if there is at least one other player
		if(group_state['player_count'] > 1):
			elapsed_time = decimal.Decimal(end_time - group_state['start_time'])
			elapsed_minutes = decimal.Decimal(elapsed_time / 60)
			decimal.getcontext().rounding = decimal.ROUND_DOWN
			elapsed_minutes = round(elapsed_minutes, 0)				
			decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
			elapsed_seconds = round(decimal.Decimal(elapsed_time - (elapsed_minutes * 60)), 1)
			
			with open(ss.filepath+'report/'+ 'GroupInformation' + '.txt', 'w') as f:							
				f.write(str(elapsed_time) + " Time Elapsed: " + str(elapsed_minutes) +" minutes and " + str(elapsed_seconds) + " seconds.\n"
					   +"Orders Fufilled: " + str(len(ss.group_state['completed'])) + "\n"
					   +"Unfilled Orders: " + str(len(ss.group_state['orders'])) + "\n"
					   +"Remaining Orders Needed for Completion: " + str(ss.completed_limit - len(ss.group_state['completed']) - len(ss.group_state['orders'])))
			make_archive(ss.group_state.get('group_key')+'_report', 'zip', ss.filepath, 'report')
		advance_state()
	
def display_pr_m_code():	
	player_rejoin.render()
	st.button("CONTINUE", on_click=code_written_switch)

def code_written_switch():
	if ss.code_written:
		ss.code_written = False
	else:
		ss.code_written = True
