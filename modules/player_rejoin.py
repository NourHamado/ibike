import streamlit as st
from streamlit import session_state as ss
import random
import string
from modules import game, group

def render():

	if 'rejoin_selected' not in ss:
		ss['rejoin_selected'] = False
	if 'rejoin_assigned' not in ss:
		ss['rejoin_assigned'] = False  # Do I need this?
	if 'rejoin_view' not in ss:
		ss['rejoin_view'] = False
	if 'rejoin_group' not in ss:
		ss['rejoin_group'] = None
	if 'rejoin_name' not in ss:
		ss['rejoin_name'] = None
	if 'rejoin_role' not in ss:
		ss['rejoin_role'] = None
	if 'rejoin_player' not in ss:
		ss['rejoin_player'] = None

	game_state = game.load()
	groups = game_state['groups']
	num_groups = len(groups)

	if ss.rejoin_selected:
		rejoin_check()

	cols = st.columns(num_groups)
	for i in range(num_groups):
		group_state = group.load(groups[i])
		with cols[i]:
			if group_state['player_count'] == 0:
				st.write("No users have joined this group.")
			for j in range(group_state['player_count']):
				num = j+1
				label = 'User '+str(num)
				pname = 'p'+str(num)+'_name'
				prole = 'p'+str(num)+'_role'
				name = group_state[pname]
				role = group_state[prole]
				if name == ss.name and role == ss.role:
					col1, col2 = st.columns(2)
					with col1:
						#st.button('Generate Code', on_click=lambda: (rejoin_begin(groups[i], name, role, num), switch_rejoin_view()))
						st.button('Generate Code', on_click=rejoin_begin, args=(groups[i], name, role, num))
						switch_rejoin_view()
	
	if ss.rejoin_view:
		if len(game_state['rejoin_codes']) == 0:
			st.write("")
		else:
			for dict in game_state['rejoin_codes']:
				if dict['player'] == ss.rejoin_player:
					st.title(f"Your Rejoin code is {dict['code']}")

	st.write("If you get disconnected from your session for any reason, use the rejoin code to reconnect to your dashboard.")
	st.write("Double click 'Generate Code' to get the code and view it. Please, write the code down")
	st.write("NOTE:  The rejoin code contains ONLY lowercase letters and integers 0 - 9.")

def rejoin_begin(group_key, name, role, num):
	ss.rejoin_group = group_key
	ss.rejoin_name = name
	ss.rejoin_role = role
	ss.rejoin_player = num
	ss.rejoin_selected = True

def rejoin_check():
	game_state = game.load()
	rejoin_dicts = game_state['rejoin_codes']
	code_exists = False
	for dict in rejoin_dicts:
		if ss.rejoin_group == dict['group'] and ss.rejoin_name == dict['name'] and ss.rejoin_role == dict['role']:
			code_exists = True
		
	if code_exists:
		st.write("")
	else:
		code_assign()

def code_assign():

	code = get_code()
	
	game_state = game.load()
	
	if len(game_state['rejoin_codes']) > 0:
		codes = []
		for dict in game_state['rejoin_codes']:
			codes.append(dict['code'])
		while code in codes or code == game_state['teacher_code']:
			code = get_code()
			
	rejoin_dict = {
		'code' : code,
		'group' : ss.rejoin_group,
		'name' : ss.rejoin_name,
		'role' : ss.rejoin_role,
		'player' :ss.rejoin_player
	}

	game_state = game.load()
	game_state['rejoin_codes'].append(rejoin_dict)
	game.save_game_state(game_state)

	ss.rejoin_selected = False
	ss.rejoin_assigned = True

def get_code():

	letters = random.choices(string.ascii_uppercase, k=3)
	numbers = random.choices(string.digits, k=3)
	characters = letters + numbers
	random.shuffle(characters)
	code = ''.join(characters)

	return code.lower()

def switch_rejoin_view():
	
	if ss.rejoin_view:
		ss.rejoin_view = False
	else:
		ss.rejoin_view = True

def display_rejoin_page():

	st.title("User Rejoin Page")
	st.write("Your instructor can provide you with a code to rejoin your session.")
	st.write("If you have trouble submitting your code, refreshing the page should fix the issue.")
	
	with st.form("rejoin_form"):
		code_query = st.text_input("Enter your rejoin code:", key='code_input')
		code_submission = st.form_submit_button("Submit")
		if (code_submission and len(code_query) > 0):
			sync_player()
			st.experimental_rerun() #causes the submit button to only need to be pressed once

def sync_player():

	game_state = game.load()
	code_matched = False
	if ss.code_input == game_state['teacher_code']:
		# write code to sync teacher here
		ss.setup_complete = True
		ss.group = 'instructor'
		ss.name = game_state['teacher_id']
		ss.role = 'instructor'
		ss.order_limit = game_state['order_limit']
		ss.completed_limit = game_state['completed_limit']
		ss.welcomed = True
		ss.rejoining = False
		ss.is_instructor = True
		ss.code_written = True
		ss.game_state = game_state
	else: 
		for dict in game_state['rejoin_codes']:
			if ss.code_input == dict['code']:
				rejoin_dict = dict
				code_matched = True
		if not code_matched:
			st.write("I'm sorry, but the code you entered does not match any existing rejoin codes. Please re-enter your code, and note that all rejoin codes contain only lowercase letters and integers 0 - 9.")
		else:
			ss.setup_complete = True
			ss.group = rejoin_dict['group']
			ss.name = rejoin_dict['name']
			ss.role = rejoin_dict['role']
			ss.order_limit = game_state['order_limit']
			ss.completed_limit = game_state['completed_limit']
			ss.group_state = group.load(ss.group)
			ss.filepath = 'files/data/'+ss.group+'/'
			ss.player = dict['player']
			ss.welcomed = True
			ss.rejoining = False
	
			game_state['rejoin_codes'].remove(rejoin_dict)
			game.save_game_state(game_state)