import random as ran
import streamlit as st
from streamlit import session_state as ss

# This module contains functions to create and manipulate an 'order' dictionary. Each order
# represents a customer order for iBIKE. Currently, the orders are generated with a random
# type and 3 random preferences from the user. The preferences will be unique for each order
# and will contain two preferences specific to the bike type and one that is independent of 
# bike type. Order will also be generate with a 'status' key that is initialized with a value
# of 'in progress'. The iBIKE game should eventually contain mechanisms to change that status to
# 'completed'
# This module is ONLY for generating a random order dictionary. group.py will
# make use of this module and will save orders to the group_state.

def Compelation():
	type_options = ['fast', 'standard']
	process = ran.choice(type_options)
	return process

def get_type():
	# function to generate random bike type
	# to be called in init()
	type_options = ['Road','Mountain','City']
	type = ran.choice(type_options)
	return type
	
def get_sprefs(type):
	# function to generate to rendom, unique preferences that are specific to the bike type
	# to be called in init()--needs bike type as an argument
	if type == 'Road':
		pref_options = ['High Speed',
						'Built for traveling long distances',
						'Aerodynamic',
						'Allows the rider to bend forward rather than sitting upright',
						'Clip-in pedals',
						'Has a handlebar that supports the rider with a variety of hand posititons',
					   ]
		
	elif type == 'Mountain':
		pref_options = ['Off road racing',
						'Is able to absorb shocks or vibrations from jumping or riding on uneven terrain',
						'Ability to take punishment on challenging terrains',
						'Large tires with a lot of traction',
						'Powerful brakes to stop while going down hills',
						'Ability to take punishment on challenging terrains',
						'A flat handle bar that allows the customer to keep a down hand position inline with the stem',
						'A slack head angle and long wheelbase for stability during descents',
					   ]
	
	else:
		pref_options = ['Easy to pedal',
						'Used mostly for paved roads but can be riden on gentle trails',
						'Practical, and built for comfort',
						'Allows for rider to sit upright rather than forward',
						'Can accommodate higher weights',
					   ]
	
	spref1 = ran.choice(pref_options)
	pref_options.remove(spref1)
	spref2 = ran.choice(pref_options)
	
	return spref1, spref2

def get_gpref():
	# generates a random preference that is applicable to all bike types
	# to be called in init()
	
	pref_options = ['Easy to control whilst cycling',
					'Easy to maintain',
					'Comfortable to ride',
					'High Quality',
					'Low Cost']
	
	pref = ran.choice(pref_options)
		
	return pref
	
"""		
def to_string(order_key):
	# outputs order to a string. Needs 'key' input where key is . . .
	# 'order1', 'order2', etc.

	### NOTE:  NEEDS TO LOAD ORDER FROM GROUP_STATE (not yet implemented)
	string_out = f"The customer wants a {order['type']} bike with the following features:"
	string_out += f"\n\t-- {order['spref1']}"
	string_out += f"\n\t-- {order['spref2']}"
	string_out += f"\n\t-- {order['gpref']}"
	
	return string_out
"""

def init(order_key):
	
	# initializes and returns an order dictionary
	
	type = get_type()
	spref1, spref2 = get_sprefs(type)
	gpref = get_gpref()
	process = Compelation()
	
	order = {'key' : order_key,
		     'process' : process,
		  	 'order_completion_date' : 'undetermined',
			 'type' : type,
			 'spref1' : spref1, 
			 'spref2' : spref2,
			 'gpref' : gpref,
			 'wheel_base' : 'undetermined',
			 'total_mass' : 'undetermined',
			 'front_wheel_rad' : 'undetermined',
			 'back_wheel_rad' : 'undetermined',
			 'status' : 'unfulfilled',
			 'checklist' : {},
			}

	for role in ss.roles:
		order['checklist'][role] = False

	return order
