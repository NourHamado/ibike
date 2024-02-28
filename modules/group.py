from modules import order
import json
import os
import streamlit as st
from streamlit import session_state as ss

# this module is designed to create, access, and update the "group_sate" for a group of
# 5 students (the player limit for one iBIKE game). The group_state is stored as a ditionary
# object in files/groupX/group_state.json, where X is the group number. All methods that
# save/load information about group states are accessing and updating that json file.

def init(group_key):
	# initializes and saves a new group_state to groupX.json, where X is the group number
	# key should be 'group1', 'group2', etc. Values to be assigned/saved later will be
	# initialized as None. Each group_state will expect a group of 5 players, with corresponding
	# names and roles to be typed/chosen in-game
	# make/store path for directory and json file for easy access
	dirpath = 'files/data/'+group_key
	filepath = dirpath+'/'+group_key+'_state.json'

	group_state = {'group_key' : group_key, 
				   'player_count' : 0,
				   'p1_name' : None,
				   'p1_role' : None,
				   'p2_name' : None,
				   'p2_role' : None,
				   'p3_name' : None,
				   'p3_role' : None,
				   'p4_name' : None,
				   'p4_role' : None,
				   'p5_name' : None,
				   'p5_role' : None,
				   'order_count' : 0,
				   'orders' : {},
				   'completed' : {},
				   'status' : 'waiting',
				   'filepath' : filepath,
				   'available_roles' : ss.roles,
				   'roles_reported' : list((True, True, True, True))
		      }
	os.mkdir(dirpath)
	with open(filepath,'w') as file:
		json.dump(group_state,file)
	return group_state

def load(group_key):
	dirpath = 'files/data/'+group_key
	filepath = dirpath+'/'+group_key+'_state.json'
	try:
		with open(filepath,'r') as file:
			group_state = json.load(file)
	except:
		return None
	else:
		return group_state

def save_group_state(group_state):
	group_key = group_state['group_key']
	dirpath = 'files/data/'+group_key
	filepath = dirpath+'/'+group_key+'_state.json'
	with open(filepath,'w') as file:
		json.dump(group_state, file)

def save_group_value(group_key,key,value):
	dirpath = 'files/data/'+group_key
	filepath = dirpath+'/'+group_key+'_state.json'
	group_state = load(group_key)
	group_state[key] = value
	with open(filepath,'w') as file:
		json.dump(group_state, file)

def add_new_order(group_key):
	dirpath = 'files/data/'+group_key
	filepath = dirpath+'/'+group_key+'_state.json'
	group_state = load(group_key)
	group_state['order_count'] += 1
	order_key = 'order'+str(group_state['order_count'])
	new_order = order.init(order_key)
	group_state['orders'][order_key] = new_order
	with open(filepath,'w') as file:
		json.dump(group_state, file)

