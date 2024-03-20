import streamlit as st
from streamlit import session_state as ss
from modules import group, player, rejoin, game
import numpy as np
import pandas as pd
import time
import decimal
import os
from os import path

def render():

	if 'part_ordered' not in ss:
		ss['part_ordered'] = False
	if 'part_cost' not in ss:
		ss['part_cost'] = 0.0

	st.title('Purchasing Manager')
	
	st.write("Welcome to the Purchasing Manager Page!")

	st.markdown(
		"""
		Your role revolves around monitoring the order quantities selected by the :blue[Industrial Engineer], 
		the annual demand, the ordering cost, and the holding cost. The :red[Economic Order Quantity (EOQ)] will
		be calculated for you, and your task will be to give feedback to the :blue[Industrial Engineer] on their
		performance.
		""")

	parts = ['Frame',
			'Handlebars',
			'Stem',
			'Suspension Fork',
			'Disc Brake Rotor',
			'Tire',
			'Rim',
			'Hub',
			'Spoke',
			'Pedal',
			'Crank Arm',
			'Crank Set',
			'Cassette',
			'Chain',
			'Seat Post',
			'Seat',
			]

	st.markdown('---')
	
	player.display_current_orders()
	
	st.markdown('---')
	
	vendors = ['GoBike', 'FastBike', 'LazyBiker']
	st.markdown('**:blue[Select Vendor]**')
	vendor = st.selectbox('Vendor',
						options=vendors,
						label_visibility='collapsed')
	if vendor == 'GoBike':
		seed = 123
	elif vendor == 'FastBike':
		seed = 321
	else:
		seed = 512
	np.random.seed(seed)
	ordering_cost = np.random.randint(10, 1000, size=(len(parts)))
	holding_cost = np.round(0.05 * ordering_cost, 2)
	annual_demand = np.random.randint(100, 10000, size=(len(parts)))
	distance = np.random.randint(500, 7000)
	lead_time = ((distance / 100) * np.random.uniform(20, 50, size=(len(parts)))) / 24

	eco_df = pd.DataFrame({'Part': parts,
							'Ordering Cost ($)': ordering_cost,
							'Annual Demand': annual_demand,
							'Holding Cost ($)': holding_cost,
							'Distance (miles)': distance,
							'Lead Time (Days)': np.round(lead_time, 2)
							})

	eco_df.index = list(range(1, len(eco_df)+1))
	st.write('')
	with st.expander('Expand to see the part economics table'):
		st.write('**:blue[Part Economics Table]**')
		st.dataframe(eco_df, width=3000)

	st.markdown('---')
	st.write('')
	if path.isfile(ss.filepath + 'orders.csv'):
		orders = pd.read_csv(ss.filepath + 'orders.csv')
		orders.index = list(range(1, len(orders)+1))
		orders = orders.merge(eco_df, on='Part', how='left')
		orders['Ordering Cost ($)'] *= orders['Qty']
		orders['Holding Cost ($)'] *= orders['Qty']
		orders['EOQ'] = round(np.sqrt((2*orders["Ordering Cost ($)"]*orders['Annual Demand'])/orders["Holding Cost ($)"]), 3)
		orders.index = list(range(1, len(orders)+1))
		
		st.write('**Orders by the :blue[Industrial Engineer]**')
		st.dataframe(orders, width=3000)

		st.markdown('---')
		total_order_cost = round(orders["Ordering Cost ($)"].sum(),2)
		total_hold_cost = round(orders["Holding Cost ($)"].sum(),2)
		total_ann_demand = orders['Annual Demand'].sum()

		st.write(f'Total Ordering Cost: **:red[${total_order_cost:,}]**')
		st.write(f'Total Holding Cost : **:red[${total_hold_cost:,}]**')
		#st.write(f'Total Annual Demand: **:red[{total_ann_demand:,}]**')
		#st.write(f'**:blue[Economic Order Quantity]: :red[{round(np.sqrt((2*total_order_cost*total_ann_demand)/total_hold_cost), 2):,}]**')
		st.markdown('---')

		if path.isfile('vendors.csv'):
			if st.button('Reset Vendor Selection!'):
				os.system('rm vendors.csv')
				vendor_df = pd.DataFrame(columns=['Part', 'Vendor'])
			else:
				vendor_df = pd.read_csv('vendors.csv')
		else:
			vendor_df = pd.DataFrame(columns=['Part', 'Vendor'])

		st.markdown('**:blue[Select vendor for each part]**')
		ordered_parts = orders.Part.tolist()
		col1, col2 = st.columns(2)
		with col1:
			part_for_vendor = st.selectbox('Part for vendor',
											options=['Select Part'] + ordered_parts,
											label_visibility='collapsed',)
		with col2:
			vendor_for_part = st.radio('Vendor for part',
										options=vendors,
										label_visibility='collapsed',)
		
		if part_for_vendor != 'Select Part':
			vendor_df.loc[len(vendor_df), :] = [part_for_vendor, vendor_for_part]
			vendor_df = vendor_df.drop_duplicates(subset='Part', keep='last')
			vendor_df.index = list(range(1, len(vendor_df)+1))
			vendor_df.to_csv('vendors.csv', index=False)

	#since vendor_df must exist, it is submitted here if group_state indicates that it should be
			group_state = group.load(ss.group_state.get('group_key'))
			if(group_state['roles_reported'][3] == False):
				submit_report_info(vendor_df, group_state)

		if len(vendor_df) > 0:
			st.dataframe(vendor_df, width=3000)

		with st.expander('Give Feedback!'):
			if path.isfile('purchasing_manager_feedback'):
				with open('purchasing_manager_feedback', 'rb') as f:
					previous_feedback = f.read().decode()
				feedback = st.text_area('feedback ...',
										value=previous_feedback,
										label_visibility='collapsed')        
			else:
				feedback = st.text_area('feedback ...',
										value='Your feedback...',
										label_visibility='collapsed')
			with open('purchasing_manager_feedback', 'w') as f:
				f.write(feedback)
	
def feedback():
	st.header("Feedback **:red[TO]**")

	text = ""
	if path.isfile(ss.filepath+'fb_pum_d.txt'):
		with open(ss.filepath+'fb_pum_d.txt', 'r') as f:
			text = f.read()

	with st.form("pur_des_feedback"):
		fb_pum_d = st.text_area("Your feedback to the Design Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pum_d != ""):
			with open(ss.filepath+"fb_pum_d.txt", "w") as f:
				f.write(fb_pum_d)
			st.experimental_rerun() #causes the submit button to only need to be pressed once
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_pum_d.txt'):
				os.remove(ss.filepath+'fb_pum_d.txt')
			st.experimental_rerun() #causes the submit button to only need to be pressed once
	
	text = ""
	if path.isfile(ss.filepath+'fb_pum_i.txt'):
		with open(ss.filepath+'fb_pum_i.txt', 'r') as f:
			text = f.read()

	with st.form("pur_ind_feedback"):
		fb_pum_i = st.text_area("Your feedback to the Industrial Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pum_i != ""):
			with open(ss.filepath+"fb_pum_i.txt", "w") as f:
				f.write(fb_pum_i)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_pum_i.txt'):
				os.remove(ss.filepath+'fb_pum_i.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_pum_pm.txt'):
		with open(ss.filepath+'fb_pum_pm.txt', 'r') as f:
			text = f.read()

	with st.form("pur_proj_feedback"):
		fb_pum_pm = st.text_area("Your feedback to the Project Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pum_pm != ""):
			with open(ss.filepath+"fb_pum_pm.txt", "w") as f:
				f.write(fb_pum_pm)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_pum_pm.txt'):
				os.remove(ss.filepath+'fb_pum_pm.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_pum_m.txt'):
		with open(ss.filepath+'fb_pum_m.txt', 'r') as f:
			text = f.read()

	with st.form("pur_mech_feedback"):
		fb_pum_m = st.text_area("Your feedback to the Mechanical Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_pum_m != ""):
			with open(ss.filepath+"fb_pum_m.txt", "w") as f:
				f.write(fb_pum_m)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_pum_m.txt'):
				os.remove(ss.filepath+'fb_pum_m.txt')
			st.experimental_rerun()
	
	# reading
	st.header("Feedback **:red[From]**")
	st.markdown("---")
	if path.isfile(ss.filepath+'fb_d_pum.txt'):
		st.write("Feedback from the **:red[Design Engineer]**:")
		with open(ss.filepath+'fb_d_pum.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_i_pum.txt'):
		st.write("Feedback from the **:red[Industrial Engineer]**:")
		with open(ss.filepath+'fb_i_pum.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_pm_pum.txt'):
		st.write("Feedback from the **:red[Project Manager]**:")
		with open(ss.filepath+'fb_pm_pum.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_m_pum.txt'):
		st.write("Feedback from the **:red[Mechanical Engineer]**:")
		with open(ss.filepath+'fb_m_pum.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

def order_part():

	ss.part_ordered = True

	parts = ['Frame',
			'Handlebars',
			'Stem',
			'Suspension Fork',
			'Disc Brake Rotor',
			'Tire',
			'Rim',
			'Hub',
			'Spoke',
			'Pedal',
			'Crank Arm',
			'Crank Set',
			'Cassette',
			'Chain',
			'Seat Post',
			'Seat',
			]
#Actual bike part prices as found on bikeparts.com 	
	MountainPrices = [2250.00,
					 168.30,
					 109.99,
					 958.00,
					 49.99,
					 185.00,
					 105.90,
					 565.90,
					 8.00,
					 35.99,
					 86.99,
					 216.95,
					 83.68,
					 25.64,
					 59.99,
					 52.79,
					 ]
	
	FastPrices = [5500.00,
				 129.99,
				 119.99,
				 1099.99,
				 55.99,
				 89.99,
				 74.99,
				 588.00,
				 8.00,
				 37.00,
				 110.00,
				 216.95,
				 93.87,
				 55.45,
				 62.10,
				 59.99,
				 ]
	
	LazyPrices = [1350.00,
				 34.58,
				 49.99,
				 549.00,
				 43.00,
				 62.95,
				 59.90,
				 130.00,
				 8.00,
				 12.36,
				 68.53,
				 100.00,
				 39.99,
				 30.00,
				 58.99,
				 50.00
				 ]
	
	idx = parts.index(ss.part_choice)
	
	if ss.vendor_choice == 'GoBike':
		price = MountainPrices[idx]

	if ss.vendor_choice == 'FastBike':
		price = FastPrices[idx]

	if ss.vendor_choice == 'LazyBike':
		price = LazyPrices[idx]

	ss.part_cost = price

def submit_report_info(vendor_df, group_state):
	group_state = group.load(ss.group_state.get('group_key'))
	if not os.path.exists(ss.filepath+'report/'):
		os.makedirs(ss.filepath+'report/')
		
	elapsed_time = decimal.Decimal(time.time() - group_state['start_time'])
	elapsed_minutes = decimal.Decimal(elapsed_time / 60)
	decimal.getcontext().rounding = decimal.ROUND_DOWN
	elapsed_minutes = round(elapsed_minutes, 0)				
	decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
	elapsed_seconds = round(decimal.Decimal(elapsed_time - (elapsed_minutes * 60)), 1)

	try:
		with open(ss.filepath+'fb_pum_d.txt', 'r') as f:
			fb_pum_d = f.read()

		with open(ss.filepath+'fb_pum_i.txt', 'r') as f:
			fb_pum_i = f.read()
		
		with open(ss.filepath+'fb_pum_pm.txt', 'r') as f:
			fb_pum_pm = f.read()

		with open(ss.filepath+'fb_pum_m.txt', 'r') as f:
			fb_pum_m = f.read()
	
	except FileNotFoundError:
		pass
	except:
		print('An error occurred')

	with open(ss.filepath+'report/'+ 'PurchasingManager' + '.txt', 'w') as f:
		f.write(ss.group + ': Purchasing Manager: '+ ss.name +'\n')
		f.write(str(elapsed_time) + " Time Elapsed: " + str(elapsed_minutes) +" minutes and " + str(elapsed_seconds) + " seconds.\n")
		f.write(vendor_df.to_string(index=False))
		f.write('\n' + '\n' + 'Feedback to the Design Engineer: '+ fb_pum_d+ '\n' +
                'Feedback to the Indistrial Engineer: '+ fb_pum_i + '\n' +
                'Feedback to the Project Manager: '+ fb_pum_pm + '\n' +
                'Feedback to the Mechanical Manager: '+ fb_pum_m)
	group_state['roles_reported'][3] = True
	group.save_group_state(group_state)
	print("Purchasing Manager submitted the report successfully")
