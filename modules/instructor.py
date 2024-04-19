import streamlit as st
from streamlit import session_state as ss
from modules import game, group, rejoin, Button_Format as format
import time
import shutil
import os
import numpy as np
import matplotlib.pyplot as plt

format.Button_Format()

def game_reset():
	dirpath = 'files/data'
	if os.path.exists(dirpath):
		shutil.rmtree(dirpath)
	os.mkdir(dirpath)
	for key in ss.keys():
		del ss[key]
	#st.caching.clear_cache()  get streamlit to delete all session data?


def reset_switch():
	if ss.reset_requested:
		ss.reset_requested = False
	else:
		ss.reset_requested = True

def reset_check():
	st.write("WARNING:  Resetting the simulation will delete progress and ALL session files. Are you sure you want to reset the simulation?" )
	col1, col2 = st.columns(2)
	with col1:
		st.button("Yes", on_click=game_reset)
	with col2:
		st.button("NO", on_click=reset_switch)

def display_rejoin():	
	st.button("BACK", on_click=rejoin_switch)
	rejoin.render()

def rejoin_switch():
	if ss.rejoin_requested:
		ss.rejoin_requested = False
	else:
		ss.rejoin_requested = True

# main function to render the instructor game setup and dashboard			
def render():
	if 'setup_complete' not in ss:
		ss['setup_complete'] = False
	if 'view_group' not in ss:
		ss['view_group'] = None
	if 'reset_requested' not in ss:
		ss['reset_requested'] = False
	if 'rejoin_requested' not in ss:
		ss['rejoin_requested'] = False
	if 'code_written' not in ss:
		ss['code_written'] = False

	if not ss.setup_complete:
		if not ss.name:
			print("No Back Button")
		elif not ss.game_state:
			st.button("BACK", on_click=name_switch)
		elif not ss.setup_complete:
			st.button("BACK", on_click=group_switch)
		st.title('iBIKE Simulation Setup')
		st.markdown('On this page, you will specify the number of student groups participating in the simulation. Each group must have 5 (and no more than 5) students. You will be able to monitor the groups\' progress, and at the end of the session, download each group\'s data.')
		init()

	elif not ss.code_written:
		st.button("BACK", on_click=complete_switch)
		display_teacher_code()

	elif ss.reset_requested:
		reset_check()

	elif ss.rejoin_requested:
		display_rejoin()

	else:
		st.button("Back", on_click=code_written_switch)
		col1, col2 = st.columns(2)
		
		with col1:
			st.button("SIMULATION RESET", on_click=reset_switch)
		with col2:
			st.button("GENERATE REJOIN CODE", on_click=rejoin_switch)
	
		if ss.setup_complete:
			dashboard()
	
			while True:
				time.sleep(5)
				st.experimental_rerun()
# Callback function to generate group_state and game_state files to manage the game
#	and to flag the game setup as complete.
def game_state_assign():
	try:
		group_num = int(ss.group_num_input)
	except:
		st.write('Please enter an integer between 1 and 10 for your group number.')
	else:
		game_state = game.init(ss.name, group_num)
		ss.game_state = game_state


def init():
	# function for instructor setup. Includes setting the instructor name and number of groups.
	if not ss.name:
		with st.form("name_form"):
			name_query = st.text_input("What is your name?")
			name_submission = st.form_submit_button("Submit")
			if (name_submission):
				if (name_query == "Nour" or name_query == "Faisal Aqlan" or name_query == "Mohammad Rasouli" or name_query == "Chetan Nikhare" or name_query =="Matthew Swinarski" or name_query == "Rumena"):
					ss.name = name_query
					st.experimental_rerun() #causes the submit button to only need to be pressed once
				else:
					st.write("You can not be the instructor. wait for your instructor to start the game")
			'''if (name_submission and len(name_query) > 0 and name_query == "Nour"):
				ss.name = name_query
				st.experimental_rerun() #causes the submit button to only need to be pressed once
			else:
				st.write("You can not be the instructor. wait for your instructor to start the game")'''

	elif not ss.game_state:
	#group_num = st.text_input('How many student groups do you have?', key='group_num_input', on_change=game_state_assign)
		#st.button("BACK", on_click=name_switch)
		with st.form("name_form"):
			group_query = st.text_input("How many student groups do you have?")
			group_submission = st.form_submit_button("Submit")
			if (group_submission):
				try:
					group_num = int(group_query)
				except:
					st.write('Please enter an integer between 1 and 10 for your group number.')
				else:
					game_state = game.init(ss.name, group_num)
					ss.game_state = game_state
					st.experimental_rerun() #causes the submit button to only need to be pressed once
		
	elif not ss.setup_complete:
		#st.button("BACK", on_click=group_switch)
		st.write("Please specify the limit of concurrent, unfulfilled customer orders that you would like to allow, along with the total number of fulfilled orders required to complete the simulation.\nWhen you are done, click \'Complete Setup\' below.")
		st.slider("Concurrent Unfulfilled Order Limit",min_value=0,max_value=100,value=25,step=5,key='order_limit_input')
		st.slider("Fulfilled Orders Required to Complete the Simulation",min_value=0,max_value=500,value=100,step=10,key='completed_limit_input')
		st.button("Complete Setup", on_click=complete_game_setup)
	
def name_switch():
	if ss.name:
		ss.name = False
	else:
		ss.name = True

def group_switch():
	if ss.game_state:
		ss.game_state = False
	else:
		ss.game_state = True

def complete_switch():
	if ss.setup_complete:
		ss.setup_complete = False
	else:
		ss.setup_complete = True

def complete_game_setup():
	ss.order_limit = ss.order_limit_input
	ss.game_state['order_limit'] = ss.order_limit_input
	ss.completed_limit = ss.completed_limit_input
	ss.game_state['completed_limit'] = ss.completed_limit_input
	game.save_game_state(ss.game_state)
	ss.setup_complete = True

def display_groups():
	game_state = game.load()
	groups = game_state['groups']
	num = len(groups)
	cols = st.columns(4, gap='large')

	p_roles = ['p1_role','p2_role','p3_role','p4_role','p5_role']
	p_names = ['p1_name','p2_name','p3_name','p4_name','p5_name']
	for i in range(0, num, 4):
		for j in range(4):
			if i + j < num:
				group_state = group.load(groups[i + j])
				with cols[j]:
					st.title("GROUP "+str(i+j+1))
					st.write(f"User Count: {group_state['player_count']}")
					st.write(f"Group Status: {group_state['status']}")
					st.write(f"Current Orders: {len(group_state['orders'])}")
					st.write(f"Completed Orders: {len(group_state['completed'])}")
					for role in ss.roles:
						name = None
						for p_role in p_roles:
							if role == group_state[p_role]:
								idx = p_roles.index(p_role)
								name = group_state[p_names[idx]]
						if name:
							st.write(role+':  '+name)
						else:
							st.write(role+':  unfilled')
					try:
						with open(group_state.get('group_key') + '_report.zip', 'rb') as f:
							st.download_button('Download Group Report', f, file_name=group_state.get('group_key') + '_report.zip')
					except FileNotFoundError:
						pass
					except:
						print('An error occurred with the ' + group_state.get('group_key') + ' report.')
		st.write("")					
		st.write("")

def dashboard():
	# function to, upon setup completion, display the instructor dashboard for the rest of the game.
	st.title('iBIKE Instructor Dashboard')
	st.write(f'Instructor name:  {ss.name}')
	st.write(f"Number of student groups: {ss.game_state['group_num']}")
	
	display_groups()
	st.title("Click on one of groups below to view their order progress.")
	display_group_options()

	if ss.view_group:
		display_group_graph(ss.view_group)
	
	#time.sleep(5)
	#st.experimental_rerun()

def view_group(group_key):
	ss.view_group = group_key

def display_group_options():
	groups = ss.game_state['groups']
	num = len(groups)
	rows = num // 5 + (num % 5 != 0)
	for i in range(rows):
		cols = st.columns(5)
		for j in range(5):
			index = i * 5 + j
			if index < num:
				with cols[j]:
					st.button(f"{groups[index]}", on_click=view_group, args=(groups[index], ))
			else:
				break

def display_group_graph(group_key):
	group_state = group.load(group_key)
	
	st.title(f"Displaying Info for {group_key}")
	st.write('Total Number of Unfulfilled Orders: '+str(len(group_state['orders'])))
	st.write('Total Number of Completed Orders: '+str(len(group_state['completed'])))
	
	data = np.array([0, 0, 0, 0, 0])
	for i in range(5):
		count = 0
		for key in group_state['orders']:
			current = group_state['orders'][key]['checklist'][ss.roles[i]]
			if i == 0 and not current:
				data[i] += 1
			else:
				previous = group_state['orders'][key]['checklist'][ss.roles[i-1]]
				if previous and not current:
					data[i] += 1
						
	inds=range(len(data))
	fig,ax = plt.subplots(figsize=(10,4))
	rects = ax.bar(inds, data, width=0.5)
	ax.set_xticks([ind for ind in inds])
	ax.set_xticklabels(ss.roles)

	plt.xticks(rotation=60, ha="right")
	plt.title(f"Current Orders Distribution for {group_key}")
	ax.set_ylabel("Orders Waiting for Processing")
	st.pyplot(fig)

def display_teacher_code():	
	game_state = game.load()
	code = game_state['teacher_code']
	st.title(f"Instructor Rejoin Code:  {code}")
	st.write("If you get disconnected from your session for any reason, use the code above to reconnect to the instructor dashboard.")
	st.write("Please write down your code, and click 'CONTINUE' when you have done so.")
	st.write("NOTE:  Your instructor code contains ONLY lowercase letters and integers 0 - 9.")

	st.button("CONTINUE", on_click=code_written_switch)

def code_written_switch():
	if ss.code_written:
		ss.code_written = False
	else:
		ss.code_written = True
		