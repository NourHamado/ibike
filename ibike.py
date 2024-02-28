import streamlit as st
from streamlit import session_state as ss
import os
import shutil
from modules import instructor, player, game, rejoin

def switch_welcome():
	ss.welcomed = True

def switch_rejoin():
	ss.rejoining = True
	ss.welcomed = True

def refresh():
	st.write('page has been refreshed')

def game_reset():
	dirpath = 'files/data'
	shutil.rmtree(dirpath)
	os.mkdir(dirpath)
	for key in ss.keys():
		del ss[key]

def display_developer_buttons():
	col1, col2 = st.columns(2)
	with col1:
		st.button("REFRESH", on_click=refresh)
	with col2:
		st.button("SIMULATION RESET", on_click=game_reset)

def welcome_instructor():

	st.write('# Welcome to iBIKE! 👋')

	st.markdown(
    """
    iBIKE is an online simuation developed to create 
    an environment for **Mechanical Engineers**, **Design Engineers**, 
    **Industrial Engineers**, **Project Managers**, and **Purchasing Managers** to practice their decision-making skills
    in selecting the appropriate parts, their order quantities, best materials 
    and manufacturing processes, parcticing supply chain management, and more.
    """
	)
	st.write("**A message for the instructors: You have the option to access the instructions by downloading the Word file provided for instructional guidance.**")
	github_url = f"https://github.com/AqlanLabRepos/ibike/raw/main/modules/Instruction%20for%20instructor.docx"
	st.markdown(f'<a href="{github_url}" download>Instructions for instructors</a>', unsafe_allow_html=True)

	st.markdown("""
        In this simulation, you will serve as the instructor, and your participants will select a group to join and potentially participate in a survey.
	After that the users have the opportunity to assume roles such as **Project Manager**, **Design Engineer**, **Mechanical Engineer**, **Industrial Engineer**, and **Purchasing Manager**. The game concludes after a predetermined number of completed customer orders that you get to set.
	Below is a flowchart illustrating how the game operates.""")
	st.image('files/images/flowchart for ibike game (1).png')

	st.write("Click 'CONTINUE' below to begin setup.")
	st.button("CONTINUE", on_click=switch_welcome)

def welcome_player():

	st.write('# Welcome to iBIKE! 👋')

	st.markdown(
    """
    iBIKE is an online simuation developed to create 
    an environment for **Mechanical Engineers**, **Design Engineers**, 
    **Industrial Engineers**, **Project Managers**, and **Purchasing Managers** to practice their decision-making skills
    in selecting the appropriate parts, their order quantities, best materials 
    and manufacturing processes, parcticing supply chain management, and more.    
    """
	)	
	
	st.markdown("""
        In this simulation, you have the option to choose between being a 'New User' or 'Rejoining' an existing session.
	New users can select a group, potentially participate in a survey, and have the opportunity to assume roles such as **Project Manager**, **Design Engineer**, **Mechanical Engineer**, **Industrial Engineer**, and **Purchasing Manager**. The game concludes after a predetermined number of completed customer orders.
	Below is a flowchart illustrating how the game operates.""")
	st.image('files/images/flowchart for ibike game (1).png')

	st.markdown(
	"""
 	**WARNING:  Do NOT close your browser while in the iBIKE simulation! If you do close your tab by accident or get disconnected for any reason, your instructor will be able to provide you with a code to rejoin your session.**
 	"""
	)

	st.write("Are you a New User or are you Rejoining an existing iBIKE session?")
	col1, col2 = st.columns(2)
	with col1:
		st.button("NEW USER", on_click=switch_welcome)
	with col2:
		st.button("REJOINING", on_click=switch_rejoin)

def main():

	# initialize the session state variables that everyone will need
	# this should be the *smallest* collection of universal variables needed 
	# to specify the behavior of the app for a given user. Any information that
	# is not specified here will be contained in the 'group_state' and 'game_state'
	# dictionaries. See those modules in 'modules' for more details. Specific roles
	# may add other session_state variables later when their pages render.
	if 'welcomed' not in ss:
		ss['welcomed'] = False
	if 'rejoining' not in ss:
		ss['rejoining'] = False
	if 'is_instructor' not in ss:
		ss['is_instructor'] = False
	if 'name' not in ss:
		ss['name'] = None
	if 'role' not in ss:
		ss['role'] = None
	if 'group' not in ss:
		ss['group'] = None
	if 'group_state' not in ss:
		ss['group_state'] = None
	if 'game_state' not in ss:
		ss['game_state'] = None
	if 'order_limit' not in ss:
		ss['order_limit'] = None
	if 'completed_limit' not in ss:
		ss['completed_limit'] = None
	if 'game_complete' not in ss:
		ss['game_complete'] = False
		
	# this is JUST a list of the roles that the game uses. I found myself copy/pasting this in many other functions, so I put it here instead at the top of the code as universal session state variable. That way, if any role names change they can just be changed here. Other functions now just reference ss.roles if needed.
	if 'roles' not in ss:
		ss['roles'] = ['Project Manager', 'Design Engineer', 'Mechanical Engineer', 'Industrial Engineer', 'Purchasing Manager']

	# check to see if game_state file has been created. If not, it is assumed the 
	# game is starting fresh and that the first user is the instructor. 
	# (this is a crude solution that should be changed later, e.g. with a instructor code)

	# Uncomment this line of code if you want a Refresh Button and a Game Reset Button to appear on screen for easier development
	# display_developer_buttons():

	if not os.path.isfile('files/data/game_state.json') and not ss.welcomed:
		ss.is_instructor = True
		ss.role = 'instructor'
		ss.group = 'instructor'
		welcome_instructor()

	elif ss.welcomed and ss.is_instructor:
		instructor.render()

	elif not ss.welcomed and not ss.is_instructor:
		welcome_player()

	elif ss.welcomed and not ss.rejoining:
		player.render()

	elif ss.welcomed and ss.rejoining:
		rejoin.display_rejoin_page()

if __name__ == '__main__':
	main()
