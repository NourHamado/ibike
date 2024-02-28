import json
from modules import group, rejoin

def load():
	filepath = 'files/data/game_state.json'
	try:
		with open(filepath,'r') as file:
			game_state = json.load(file)
	except:
		return None
	else:
		return game_state

def save_game_state(game_state):
	filepath = 'files/data/game_state.json'
	with open(filepath,'w') as file:
		json.dump(game_state, file)

def save_game_value(key, value):
	filepath = 'files/data/game_state.json'
	game_state = load()
	game_state[key] = value
	with open(filepath,'w') as file:
		json.dump(game_state, file)

def init(name,group_num):
	filepath = 'files/data/game_state.json'
	game_state = {
		'teacher_id' : name,
		'group_num' : group_num,
		'groups' : [],
		'available_groups' : [],
		'order_limit' : None,
		'completed_limit' : None,
		'rejoin_codes' : [],
		'teacher_code' : rejoin.get_code()
	}
	
	for i in range(group_num):
		key = 'group'+str(i+1)
		group.init(key)
		game_state['available_groups'].append(key)
		game_state['groups'].append(key)
	
	with open(filepath,'w') as file:
		json.dump(game_state, file)
	return game_state