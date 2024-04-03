import streamlit as st
from streamlit import session_state as ss
from modules import group, player, player_rejoin, game
import pandas as pd
import numpy as np
import time
import decimal
import matplotlib.pyplot as plt
import os
from os import path
import seaborn as sns

def render():
	if 'code_written' not in ss:
		ss['code_written'] = False

	if not ss.code_written:
		display_i_e_code()
	else:
		st.title('Industrial Engineer')
	
		st.write("Welcome to the Industrial Engineer Page!")
		
		def forecasting(seed):
			st.markdown("---")
			np.random.seed(seed)
			with st.expander('See last N-month demand and invetory'):
				size = st.slider("Period of Visualization (Months)", 1, 12, 12)
				readings = np.random.randint(50, 400, size=(size,))
				in_stock = np.random.randint(50, 400, size=(size,))
				mean = np.mean(np.float32(readings))
				suggested_order = mean - np.float32(in_stock[-1])
				time = list(range(1-size, 1))
				fig, ax = plt.subplots()
				fig.figsize = (12, 6)
		
				data1 = pd.DataFrame({'Month':time,
									'Reading': in_stock, # inventory
									})
				data2 = pd.DataFrame({'Month':time,
									'Reading': readings, # demand
									})
		
				data = pd.concat([data1, data2], axis=0)
				data['Type'] = ['Inventory']*(len(data)//2) + ['Demand']*(len(data)//2)
		
				sns.barplot(data=data, x='Month', y='Reading', hue='Type', ax=ax, alpha=0.7)
				ax.axhline(y=mean, c='red', linestyle='--')
				st.pyplot(fig)
				st.markdown("---")
			return suggested_order
		
		st.markdown(
			"""
			Your role revolves around two main points. You will forecast the demand and then order the appropriate quantities based on the forecasting results. You will be given a dropdowm list for all the bike parts.  
		""")
		
		st.text("")

		st.title(':blue[Demand Forecasting]')

		st.markdown("""
		To forecast the demand, you will be provided with the quantities of each part per bike and
		shown the demand for the last 12 months for each part that you expand. It will show a line graph 
		encompassing the demand, the inventory level, and the moving average demand for the last 12 months. 
		We also provide you with an initial value that you can use for your prediction. The initial value is
		average demand minus the current inventory. 
		""")
		
		st.markdown("---")

		player.display_current_orders()

		st.markdown('---')

		st.markdown('#### :blue[Select Bike Parts to Order]')
		st.markdown("""
					You can do this sequentially. Each time you can select one part, then define the
					order quantity.
					""")

		parts = ['Select Part',
				'Frame',
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
		
		np.random.seed(123)
		lead_times = np.random.randint(7, 120, size=len(parts))
		
		col1, col2 = st.columns(2)

		with col1:
			part = st.selectbox(
								label='Part', 
								options=parts,
								label_visibility='collapsed',
								key=5,
								)
		
		if part != "Select Part":
			np.random.seed(123)
			seeds = np.random.randint(1, 1000, size=(len(parts),))
			idx = parts.index(part)

			with col2:
				st.markdown(f":blue[Lead time is (Days):] :red[{lead_times[idx]}]")
			seed = seeds[idx]

			st.text('')

			suggested_order = forecasting(seed)
			if suggested_order > 0:
				qty = int(suggested_order)
			else:
				qty = 0

			st.text('')
			st.markdown('#### :blue[Choose the order quantity]')
			st.markdown('The initial value given below is calculated as follows:')
			st.latex('Order = Mean~Demand - Current~Invetory')
			order_qty = st.number_input('Quantity (The initial value is = mean demand - inventory)', 
										label_visibility='collapsed',
										value=qty, min_value=0)
			st.markdown("---")

			if not path.isfile(ss.filepath+'orders.csv'):
				orders_df = pd.DataFrame(columns=['Part', 'Qty'])

			else:
				orders_df = pd.read_csv(ss.filepath+'orders.csv')

			if st.button('Reset Table', key=8):
				try:
					os.remove(ss.filepath+'orders.csv')
				except:
					pass
				part = "Select Part"
			else:
				try:
					orders_df.loc[orders_df.shape[0]] = [part, order_qty]
					orders_df = orders_df.drop_duplicates(subset=['Part'], keep='last')
					orders_df.index = range(1, orders_df.shape[0] + 1)
					orders_df.to_csv(ss.filepath+'orders.csv', index=False)

					#since orders_df must exist, it is submitted here if group_state indicates that it should be
					group_state = group.load(ss.group_state.get('group_key'))
					if(group_state['roles_reported'][2] == False):
						submit_report_info(orders_df, group_state)
				except:
					pass
		try:
			st.text('')
			st.text('')
			st.text('')
			st.write('### Your ordered parts and quantities')
			st.dataframe(orders_df, use_container_width=True)
		except:
			pass

	
def feedback():
	# writing
	st.header("Feedback **:red[TO]**")
	text = ""
	if path.isfile(ss.filepath+'fb_i_d.txt'):
		with open(ss.filepath+'fb_i_d.txt', 'r') as f:
			text = f.read()

	with st.form("ind_des_feedback"):
		fb_i_d = st.text_area("Your feedback to the Design Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_i_d != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_i_d.txt", "w") as f:
					f.write(fb_i_d)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun() #causes the submit button to only need to be pressed once
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_i_d.txt'):
				os.remove(ss.filepath+'fb_i_d.txt')
			st.experimental_rerun() #causes the submit button to only need to be pressed once


	text = ""
	if path.isfile(ss.filepath+'fb_i_m.txt'):
		with open(ss.filepath+'fb_i_m.txt', 'r') as f:
			text = f.read()

	with st.form("ind_mech_feedback"):
		fb_i_m = st.text_area("Your feedback to the Mechanical Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")

		if (feedback_submission and fb_i_m != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_i_m.txt", "w") as f:
					f.write(fb_i_m)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_i_m.txt'):
				os.remove(ss.filepath+'fb_i_m.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_i_pm.txt'):
		with open(ss.filepath+'fb_i_pm.txt', 'r') as f:
			text = f.read()

	with st.form("ind_proj_feedback"):
		fb_i_pm = st.text_area("Your feedback to the Project Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_i_pm != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_i_pm.txt", "w") as f:
					f.write(fb_i_pm)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_i_pm.txt'):
				os.remove(ss.filepath+'fb_i_pm.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_i_pum.txt'):
		with open(ss.filepath+'fb_i_pum.txt', 'r') as f:
			text = f.read()

	with st.form("ind_pur_feedback"):
		fb_i_pum = st.text_area("Your feedback to the Purchasing Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_i_pum != ""):
			with st.spinner("Submitting feedback..."):
				time.sleep(1)
				with open(ss.filepath+"fb_i_pum.txt", "w") as f:
					f.write(fb_i_pum)
				st.success("Feedback sent!", icon="✅")
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_i_pum.txt'):
				os.remove(ss.filepath+'fb_i_pum.txt')
			st.experimental_rerun()
	
	# reading
	st.header("Feedback **:red[From]**")
	st.markdown("---")
	if path.isfile(ss.filepath+'fb_d_i.txt'):		
		st.write("Feedback from the **:red[Design Engineer]**:")
		with open(ss.filepath+'fb_d_i.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_m_i.txt'):
		st.write("Feedback from the **:red[Mechanical Engineer]**:")
		with open(ss.filepath+'fb_m_i.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_pm_m.txt'):
		st.write("Feedback from the **:red[Project Manager]**:")
		with open(ss.filepath+'fb_pm_m.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")


	if path.isfile(ss.filepath+'fb_pum_m.txt'):
		st.write("Feedback from the **:red[Purchasing Manager]**:")
		with open(ss.filepath+'fb_pum_m.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

def submit_report_info(orders_df, group_state):
	group_state = group.load(ss.group_state.get('group_key'))
	if not os.path.exists(ss.filepath+'report/'):
		os.makedirs(ss.filepath+'report/')

	elapsed_time = decimal.Decimal(time.time() - group_state['start_time'])
	elapsed_minutes = decimal.Decimal(elapsed_time / 60)
	decimal.getcontext().rounding = decimal.ROUND_DOWN
	elapsed_minutes = round(elapsed_minutes, 0)				
	decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
	elapsed_seconds = round(decimal.Decimal(elapsed_time - (elapsed_minutes * 60)), 1)

	fb_i_d = ""
	if path.isfile(ss.filepath+'fb_i_d.txt'):
		with open(ss.filepath+'fb_i_d.txt', 'r') as f:
			fb_i_d = f.read()

	fb_i_m = ""
	if path.isfile(ss.filepath+'fb_i_m.txt'):
		with open(ss.filepath+'fb_i_m.txt', 'r') as f:
			fb_i_m = f.read()
		
	fb_i_pm = ""
	if path.isfile(ss.filepath+'fb_i_pm.txt'):
		with open(ss.filepath+'fb_i_pm.txt', 'r') as f:
			fb_i_pm = f.read()

	fb_i_pum = ""
	if path.isfile(ss.filepath+'fb_i_pum.txt'):
		with open(ss.filepath+'fb_i_pum.txt', 'r') as f:
			fb_i_pum = f.read()


	with open(ss.filepath+'report/'+ 'IndustrialEngineer' + '.txt', 'w') as f:
		f.write(ss.group + ': Industrial Engineer: '+ ss.name +'\n')
		f.write(str(elapsed_time) + " Time Elapsed: " + str(elapsed_minutes) +" minutes and " + str(elapsed_seconds) + " seconds.\n")
		f.write(orders_df.to_string(index=False))
		f.write('\n' + '\n' + 'Feedback to the Design Engineer: '+ fb_i_d+ '\n' +
                'Feedback to the Mechanical Engineer: '+ fb_i_m + '\n' +
                'Feedback to the Project Manager: '+ fb_i_pm + '\n' +
                'Feedback to the Purchasing Manager: '+ fb_i_pum)
	group_state['roles_reported'][2] = True
	group.save_group_state(group_state)
	print("Industrial Engineer submitted the report successfully")

def display_i_e_code():	
	player_rejoin.render()
	st.button("CONTINUE", on_click=code_written_switch)

def code_written_switch():
	if ss.code_written:
		ss.code_written = False
	else:
		ss.code_written = True