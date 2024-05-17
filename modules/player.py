from xml.dom.minidom import Document
import streamlit as st
from streamlit import session_state as ss
from modules import game, group
import numpy as np
import matplotlib.pyplot as plt
import time
from modules import Project_Manager as pr_m, Design_Engineer as d_e, Mechanical_Engineer as m_e, Industrial_Engineer as i_e, Purchasing_Manager as pu_m
from modules import mainform as survey, form13 as form, Button_Format as format
import docx


def render():
	if 'setup_complete' not in ss:
		ss['setup_complete'] = False
	if 'order_view' not in ss:
		ss['order_view'] = False

	if not ss.setup_complete:
		init()
	else:
		st.title('iBIKE Simulation')
		st.write('Work with your team members to complete orders!')

		ss.group_state = group.load(ss.group)
		if ss.group_state['status'] != 'completed':
			format.Tab_Format()
			tab1, tab2, tab3= st.tabs(["Your Page","Feedback Page","Group Status"])
			with tab1:
				display_role_page()
			with tab2:
				display_feedback_page()
			with tab3:
				display_group_info()
		else:
			#if(ss.role == 'Purchasing Manager' or ss.role == 'Project Manager'):
			display_role_page()
			#else:
			#	display_game_complete()


	#time.sleep(30)
	#st.experimental_rerun()
	#synchronize()

# Function to be called on each user page to display widgets to select orders and pass
# them on to the next role.
def display_current_orders():
	st.write("Click the \"Refresh Orders\" button below in order to refresh your page and view current orders.")
	st.button("Refresh Orders")
	format.Button_Format()
	
	if len(ss.group_state['orders']) > 0:

		idx = ss.roles.index(ss.role)
		order_keys = []
		for order_key in ss.group_state['orders'].keys():
			if idx == 0 and not ss.group_state['orders'][order_key]['checklist'][ss.roles[idx]]:
				order_keys.append(order_key)
			elif not ss.group_state['orders'][order_key]['checklist'][ss.roles[idx]] and ss.group_state['orders'][order_key]['checklist'][ss.roles[idx-1]]:
				order_keys.append(order_key)

		if len(order_keys) > 0:
			st.write('Total Number of Unfulfilled Orders: '+str(len(ss.group_state['orders'])))
			st.write('Total Number of Completed Orders: '+str(len(ss.group_state['completed'])))
			col1, col2 = st.columns(2)
			with col1:
				idx = ss.roles.index(ss.role)
				if idx < 3:
					st.radio('Orders Ready for your input:  ', order_keys, key='order_choice')
				else:
					st.markdown(
						"""
					<style>
					span[data-baseweb="tag"] {
						background-color: #243b3b !important;
					}
					</style>
					""",
						unsafe_allow_html=True,
					)
					selected_order = st.multiselect('Orders Ready for your input:  ', order_keys)
			with col2:
				st.write('Please select an order for processing:')
				idx = ss.roles.index(ss.role)
				if idx < 3:
					if 'order_choice' in ss:
						st.button("View "+ss.order_choice, on_click=switch_order_view)
						if ss.order_view:
							st.write(ss.group_state['orders'][ss.order_choice])
						if idx < 3:
							button_text = "Send "+ss.order_choice+" to "+ss.roles[idx+1]
						st.button(button_text, on_click=move_order, args=(ss.order_choice, ))
				else:
					if selected_order:
						st.button("View selected orders", on_click=switch_order_view)
						if ss.order_view:
							for order in selected_order:
								st.write(ss.group_state['orders'][order])
						if idx == 3:
							button_text = "Send all selected orders to "+ss.roles[idx+1]
						else:
							button_text = "Complete all selected Orders"
						st.button(button_text, on_click=move_orders, args=(selected_order, ))

		else:
			st.write('There are no orders for you to work on right now.')

		display_orders_graph()
		
	else:
		st.write('There are no current customer orders. Please wait for your Project Manager to receive more orders.')


		
def display_role_page():
	if ss.role == 'Project Manager':
		pr_m.render()
	elif ss.role == 'Design Engineer':
		d_e.render()
	elif ss.role == 'Mechanical Engineer':
		m_e.render()
	elif ss.role == 'Industrial Engineer':
		i_e.render()
	elif ss.role == 'Purchasing Manager':
		pu_m.render()

  
def display_feedback_page():
	if ss.role == 'Project Manager':
		pr_m.feedback()
	elif ss.role == 'Design Engineer':
		d_e.feedback()
	elif ss.role == 'Mechanical Engineer':
		m_e.feedback()
	elif ss.role == 'Industrial Engineer':
		i_e.feedback()
	elif ss.role == 'Purchasing Manager':
		pu_m.feedback()

def display_group_info():
	p_roles = ['p1_role','p2_role','p3_role','p4_role','p5_role']
	p_names = ['p1_name','p2_name','p3_name','p4_name','p5_name']
	
	st.title("Group Information")
	st.write(f"Group Member Count: {ss.group_state['player_count']}")
	st.write(f"Group Status: {ss.group_state['status']}")
	st.write(f"Current Orders: {len(ss.group_state['orders'])}")
	st.write(f"Completed Orders: {len(ss.group_state['completed'])}")
	
	for role in ss.roles:
		name = None
		for p_role in p_roles:
			if role == ss.group_state[p_role]:
				idx = p_roles.index(p_role)
				name = ss.group_state[p_names[idx]]
		if name:
			st.write(role+':  '+name)
		else:
			st.write(role+':  unfilled')

	
	st.write("Expand the bar below to view the instruction file.")

	file_path = "instruction_file.docx"  # Path to the uploaded file

	try:
		with st.expander('Instructions for the Simulation'):
			with open(file_path, "rb") as f:
				file_contents = f.read()
			#st.download_button(label="Download DOCX", data=file_contents, file_name="uploaded_file.docx")

			# Display the content of the DOCX file
			doc = docx.Document(file_path)  # Corrected line
			#st.write("## Document Content")
			for para in doc.paragraphs:
				st.write(para.text)
	except FileNotFoundError:
		st.error("No file uploaded by the instructor yet.")

def display_game_complete():
	st.title("The Simulation is Over")
	st.write("Thank you for playing!")

# this function first checks availability and then assigns a user to a group if it is not already full.
# if a user is the 5th member of a group, that group will be removed from the available, displayed groups for all other users
def group_assign(group_key):
	group_state = group.load(group_key)
	game_state = game.load()
	groups = game_state['available_groups']
	
	ss.group = group_key
	ss['filepath'] = 'files/data/'+ss.group+'/'
	group_state['player_count'] += 1
	ss['player'] = group_state['player_count']
	if group_state['player_count'] == 1:
		group_state['start_time'] = time.time()
	elif group_state['player_count'] == 5:
		groups.remove(group_key)
		game_state['available_groups'] = groups
		game.save_game_state(game_state)
		group_state['status'] = 'in progress'
	group.save_group_state(group_state)
	
# a function to display the available groups to join based on the current state of the game.
def display_group_buttons():
	st.write(f"Hello, {ss.name}! Please select one of the available groups below:")

	game_state = game.load()
	groups = game_state['available_groups']
	num = len(groups)
	rows = num // 5 + (num % 5 != 0)

	for i in range(rows):
		cols = st.columns(5)
		for j in range(5):
			index = i * 5 + j
			if index < num:
				with cols[j]:
					st.button(f"{groups[index]}", on_click=update_init_selection, args=(0, groups[index]))
			else:
				with cols[j]:
					pass

def role_assign(role):
	group_state = group.load(ss.init_selection[0])
	roles = group_state['available_roles']
	
	ss.role = role
	roles.remove(role)
	group_state['available_roles'] = roles
	
	if ss.player == 1:
		group_state['p1_name'] = ss.name
		group_state['p1_role'] = ss.role
		group_state['start_time'] = time.time()
	elif ss.player == 2:
		group_state['p2_name'] = ss.name
		group_state['p2_role'] = ss.role
		group_state['start_time'] = time.time()
	elif ss.player == 3:
		group_state['p3_name'] = ss.name
		group_state['p3_role'] = ss.role
		group_state['start_time'] = time.time()
	elif ss.player == 4:
		group_state['p4_name'] = ss.name
		group_state['p4_role'] = ss.role
		group_state['start_time'] = time.time()
	else:
		group_state['p5_name'] = ss.name
		group_state['p5_role'] = ss.role
		group_state['start_time'] = time.time()
			
	group.save_group_state(group_state)
		
def display_role_buttons(selected_group): 
	st.write(f"Alright, {ss.name}, you have now selected {selected_group}.")    

	group_state = group.load(selected_group)
	roles = group_state['available_roles']
	num = len(roles)    
	if(num != 0):
		#text that should only print when the selection is valid
		st.write("Please select one of the available group roles below.")
		st.write("This will be your role for the rest of this session:")
		
		cols = st.columns(num)
		for i in range(num):
			with cols[i]:
				st.button(f"{roles[i]}", on_click=update_init_selection, args=(1, roles[i]))
	else:
		#edge case where the user has yet to choose a group but the last role in that group is taken just before they select the group
		ss.init_selection[0] = ''

		st.write("I'm sorry, the group you chose is full. Please select a different group.")
		st.button('Try Again')

#called by both display_buttons functions in a callback once the user has made their selection
#num indicates whether it is the group (0) or the role (1) and str contains the user's selection
def update_init_selection(num, str):
	#input validation is not needed on num or str since the user clicks buttons to select these values, not direct input
	ss.init_selection[num] = str

def check_init_selection():
	game_state = game.load()
	groups = game_state['available_groups']
	group_state = group.load(ss.init_selection[0])
	roles = group_state['available_roles']
	
	if ss.init_selection[0] not in groups:
		st.write("I'm sorry, the group you chose is full. Please select a different group.")
		return False
	elif ss.init_selection[1] not in roles:
		st.write("I'm sorry, the role you chose is already filled. Please select a different role.")
		return False
	else:
		return True

def process_init_selection():
	if(check_init_selection()):
		group_assign(ss.init_selection[0])
		role_assign(ss.init_selection[1])
		sync_game_settings()
	else:
		ss.init_selection[0] = ''
		ss.init_selection[1] = ''

		#the following button allows the user to start again by rerunning streamlit when they are ready
		st.button('Try Again')

def sync_game_settings():
	game_state = game.load()
	ss.order_limit = game_state['order_limit']
	ss.completed_limit = game_state['completed_limit']
	ss.setup_complete = True
	st.experimental_rerun()

def init():
	game_state = game.load()
	size = len(game_state['available_groups'])
	
	show_group_selection = not ss.group  # Flag to control group selection display

	if 'survey_active' not in ss:
		ss.survey_active = False;
	if 'init_selection' not in ss:
		ss.init_selection = ['', ''];

	if size == 0:
		st.write("I'm sorry, this simulation is full. Please wait for the next round")
	
	elif not ss.name:
		st.title('Welcome to the User Page!')
		st.write('On this page, you will choose your group and role.')
		
		with st.form("name_form"):
			name_query = st.text_input("What is your name?")
			name_submission = st.form_submit_button("Submit")
			if (name_submission and len(name_query) > 0):
				ss.name = name_query
				st.experimental_rerun() #causes the submit button to only need to be pressed once

	elif not ss.group and not ss.role:
		print("Survey State: " + str(ss.survey_active));
		if(not ss.survey_active):
			if(ss.init_selection[0] == ''):              
				display_group_buttons()
			elif(ss.init_selection[1] == ''):
				display_role_buttons(ss.init_selection[0])
			else:
				process_init_selection()
			st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
			col1, col2 = st.columns(2)
			with col1:
				st.button("BACK", on_click=name_switch) 
			with col2:
				st.button('I would like to take the survey', on_click=form.toggle_survey_state)
				   
		else:
			survey.main_form()

def name_switch():
	if ss.name:
		ss.name = False
	else:
		ss.name = True
		
def switch_order_view():
	if ss.order_view == True:
		ss.order_view = False
	else:
		ss.order_view = True

def move_order(order_key):
	idx = ss.roles.index(ss.role)
	# get most up-to-date group state first:
	group_state = group.load(ss.group)
	group_state['orders'][order_key]['checklist'][ss.role] = True
			
	group.save_group_state(group_state) #group state must be saved before the below call since it too modifies the group state

	if idx == 0:
		pr_m.submit_order_info(order_key)
	if idx == 1:
		d_e.submit_order_info(order_key)

def move_orders(order_keys):
	idx = ss.roles.index(ss.role)
	# get most up-to-date group state first:
	group_state = group.load(ss.group)

	for order_key in order_keys:
		group_state['orders'][order_key]['checklist'][ss.role] = True
			
		if idx == 4:
			group_state['completed'][order_key] = group_state['orders'][order_key]
			del group_state['orders'][order_key]
			if len(group_state['completed']) >= ss.completed_limit :
				group_state['status']='completed'

	group.save_group_state(group_state) #group state must be saved before the below call since it too modifies the group state

def display_orders_graph():
	data = np.array([0, 0, 0, 0, 0])
	for i in range(5):
		count = 0
		for key in ss.group_state['orders']:
			current = ss.group_state['orders'][key]['checklist'][ss.roles[i]]
			if i == 0 and not current:
				data[i] += 1
			else:
				previous = ss.group_state['orders'][key]['checklist'][ss.roles[i-1]]
				if previous and not current:
					data[i] += 1
						
	inds=range(len(data))
	fig,ax = plt.subplots(figsize=(10,4))
	rects = ax.bar(inds, data, width=0.5)
	ax.set_xticks([ind for ind in inds])
	ax.set_xticklabels(ss.roles)

	plt.xticks(rotation=60, ha="right")
	plt.title("Current Orders Distribution")
	ax.set_ylabel("Orders Waiting for Processing")
	st.pyplot(fig)

# I need a different way to automatically synchronize the group state for group members. This is causing issues with widget interaction with the rest of my code and I don't know why.
def synchronize():
	while True:
		time.sleep(5)
		group_state = group.load(ss.group)
		if group_state != ss.group_state:
			st.experimental_rerun()