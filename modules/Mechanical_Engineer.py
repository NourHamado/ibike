import pandas as pd
from os import path
import streamlit as st
import time
import decimal
from streamlit import session_state as ss
from modules import group, player, game, player_rejoin
import os

def render():
	if 'code_written' not in ss:
		ss['code_written'] = False

	if not ss.code_written:
		display_m_e_code()
	else:
		st.title('Mechanical Engineer')
		
		st.write("Welcome to the Mechanical Engineer Page!")
		# st.image('mechanical_avatar.jpg')

		st.markdown(
			"""
			Your role revolves around selecting the bike **Parts** to manufacture,
			their **Materials**, and the "Manufacturing Processes". You will be given
			each of these in a dropdown list from which you can make your selections. For each part,
			you will only be shown the most appropriate materials and manufacturing processes.
			""")

		st.markdown("---")

		player.display_current_orders()

		st.markdown('---')

		if not path.isfile(ss.filepath+'parts_selction.csv'):
			selection_df = pd.DataFrame(columns=['Part', 'Material', 'Process'])
		else:
			selection_df = pd.read_csv(ss.filepath+'parts_selction.csv')
			st.markdown("These are the previously selected parts with the materials and the manufacturing processes:")
			st.dataframe(selection_df, width=3000)
			st.markdown("---")

		if not path.isfile(ss.filepath+'parts_material_process_justification.csv'):
			justification_df = pd.DataFrame(columns=['Part', 'Material Justification', 'Process Justification'])
		else:
			justification_df = pd.read_csv(ss.filepath+'parts_material_process_justification.csv')
			st.markdown("These are the previously selected parts with justificaions for materials manufacturing processes:")
			st.dataframe(justification_df, width=3000)
			st.markdown("---")

		if path.isfile(ss.filepath+'material_feedback.csv'):
			st.markdown("Here is the feedback by the :red[Industrial Engineer] on the selected materials:")
			material_feedback_df = pd.read_csv(ss.filepath+'material_feedback.csv')
			st.dataframe(material_feedback_df, width=3000)
			st.markdown("---")

		if path.isfile(ss.filepath+'process_feedback.csv'):
			st.markdown("Here is the feedback by the :red[Industrial Engineer] on the selected manufacturing processes:")
			process_feedback_df = pd.read_csv(ss.filepath+'process_feedback.csv')
			st.dataframe(process_feedback_df, width=3000)
			st.markdown("---")

		if path.isfile('pm_feedback_mech_1'):
			st.markdown("""
						Here is the feedback by the :red[Project Manager] on the selected parts, materials, and
						manufacturing processes:""")
			with open ('pm_feedback_mech_1', 'rb') as f:
				text = f.read().decode()
			with st.expander("Expand to see feedback!"):
				st.markdown(f":red[{text}]")
			st.markdown("---")

		if path.isfile('pm_feedback_mech_2'):
			st.markdown("""
						Here is the feedback by the :red[Project Manager] on your justificaions:""")
			with open ('pm_feedback_mech_2', 'rb') as f:
				text = f.read().decode()
			with st.expander("Expand to see feedback!"):
				st.markdown(f":red[{text}]")
			st.markdown("---")

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

		col1, col2 = st.columns(2)

		with col1:
			st.markdown('### :blue[Select a part]')
			part = st.selectbox(
				label='Part', 
				options=parts,
				label_visibility='collapsed',
			)


		def make_selections(materials, processes, minimize, maximize):
			with col2:
				st.write('Objectives are:')
				st.write(f'**:red[Minimize:]** {minimize}')
				st.write(f'**:blue[Maximize:]** {maximize}')
			st.markdown("---")

			col3, col4 = st.columns(2)
			with col3:
				st.markdown('#### :blue[Select an appropriate material]')
				st.text("")
				st.text("")
				material = st.selectbox(
					label="Material",
					options=materials,
					label_visibility='collapsed',
				)
				st.text("")
				st.markdown("#### :red[Justify material selection]")
				st.text("")
				st.text("")
				material_just = st.text_area(label="", 
										value="Your justification(100 Chars Max)", 
										label_visibility="collapsed",
										max_chars=100,
										key=0,)
			
			with col4:
				st.markdown('#### :blue[Select an appropriate manufacturing process]')
				process = st.selectbox(
					label="Manufacturing Process",
					options=processes,
					label_visibility='collapsed',
				)
				st.text("")
				st.markdown("#### :red[Justify manufacturing process selection]")
				process_just = st.text_area(label="", 
											value="Your justification (100 Chars Max)", 
											label_visibility="collapsed",
											max_chars=100,
											key=1)
			st.markdown("---")
			return material, process, material_just, process_just


		if part == 'Frame':
			minimize =  'Weight (Density)'
			maximize = 'Ultimate Tensile Strength'
			materials = ['Select Material',
						'Age-Hardening Wrought Al-Alloy',
						'High Carbon Steel',
						'Low Alloy Steel',
						'Titanium Alloys',
						'Wrought Magnesium Alloys'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Drawing', 
						'Machining', 
						'Heat Treatment', 
						'Joining',
						'Surface Treatment'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Handlebars':
			minimize =  'Price'
			maximize = 'Young’s Modulus'
			materials = ['Select Material',
						'Cast Iron - Ductile (Nodular)',
						'Cast Iron - Gray',
						'High Carbon Steel',
						'Low Carbon Steel',
						'Medium Carbon Steel'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Drawing', 
						'Machining', 
						'Extrusion', 
						'Heat Treatment',
						'Joining',
						'Surface Treatment'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Stem':
			minimize =  'Price'
			maximize = 'Compressive Strength'
			materials = ['Select Material',
						'Cast Iron - Ductile (Nodular)',
						'Cast Iron - Gray',
						'High Carbon Steel',
						'Low Alloy Steel',
						'Medium Carbon Steel'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Machining',
						'Heat Treatment',
						'Joining',
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Suspension Fork':
			minimize =  'Weight (Density)'
			maximize = 'Compressive Strength'
			materials = ['Select Material',
						'Boron Carbide',
						'Silica Glass',
						'Silicon',
						'Silicon Carbide',
						'Silicon Nitride'
						]
			processes = ['Select Manufacturing Process',
						'Extrusion', 
						'Reaction Bonding',
						'Hot Pressing',
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Disc Brake Rotor':
			minimize =  'Price'
			maximize = 'Weight (Density)'
			materials = ['Select Material',
						'Cast Iron - Ductile (Nodular)',
						'Cast Iron - Gray',
						'High Carbon Steel',
						'Low Alloy Steel',
						'Low Carbon Steel'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Drawing', 
						'Machining',
						'Heat Treatment',
						'Joining',
						'Surface Treatment',
						'Casting'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)


		elif part == 'Tire':
			minimize =  'Weight (Density)'
			maximize = 'Moldability'
			materials = ['Select Material',
						'Butyl Rubber (IIR)',
						'Ethylene Vinyl Acetate (EVA)',
						'Ionomer (I)',
						'Natural Rubber (NR)',
						'Polyethylene'
						]
			processes = ['Select Manufacturing Process',
						'Polymer Injection Molding', 
						'Polymer Extrusion', 
						'Polymer Thermoforming',
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Rim':
			minimize =  'Weight (Density)'
			maximize = 'Young’s Modulus'
			materials = ['Select Material',
						'Alumina',
						'Aluminium Nitride',
						'Boron Carbide',
						'CFRP - Epoxy Matrix (Isotropic)',
						'Silicon Carbide'
						]
			processes = ['Select Manufacturing Process',
						'Ring Rolling', 
						'Casting', 
						'Forging',
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Hub':
			minimize =  'Price'
			maximize = 'Fatigue Strength at 10^7 cycles'
			materials = ['Select Material',
						'Cast Iron - Ductile (Nodular)',
						'Cast Iron - Gray',
						'High Carbon Steel',
						]
			processes = ['Select Manufacturing Process',
						'Rolling', 
						'Cold Forging (Closed Die)', 
						'Casting',
						'Drawing',
						'Swaging'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Spoke':
			minimize =  'Price'
			maximize = 'Specific Stiffness (Level 3)'
			materials = ['Select Material',
						'Cast Iron',
						'Dolomite',
						'Jute Fibre',
						'Kenaf Fibre',
						'Mica (p)'
						]
			processes = ['Select Manufacturing Process',
						'Casting', 
						'Machining'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Pedal':
			minimize =  'Price'
			maximize = 'Ultimate Tensile Strength'
			materials = ['Select Material',
						'Cast Iron - Ductile (Nodular)',
						'Cast Iron - Gray',
						'High Carbon Steel',
						'Low Alloy Steel',
						'Medium Carbon Steel'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Drawing', 
						'Machining',
						'Heat Treatment',
						'Joining',
						'Surface Treatment'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Crank Arm':
			minimize =  'Weight(Density)'
			maximize = 'Ultimate Tensile Strength'
			materials = ['Select Material',
						'Bamboo',
						'CFRP - Epoxy Matrix',
						'Low Alloy Steel',
						'Titanium alloys',
						'Wrought Magnesium Alloys'
						]
			processes = ['Select Manufacturing Process',
						'Casting', 
						'Machining'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Crank Set':
			minimize =  'Weight(Density)'
			maximize = 'Fatigue Strength at 10^7 Cycles'
			materials = ['Select Material',
						'Boron Carbide',
						'CFRP - Epoxy Matrix',
						'Silicon Nitride',
						'Titanium Alloys',
						'Wrought Magnesium Alloys'
						]
			processes = ['Select Manufacturing Process',
						'Casting', 
						'Machining'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		elif part == 'Cassette':
			minimize =  'Weight(Density)'
			maximize = 'Fatigue Strength at 10^7 Cycles'
			materials = ['Select Material',
						'Butyl Rubber (IIR)',
						'Ethylene Vinyl',
						'Acetate (EVA)',
						'Ionomer(I)',
						'Natural Rubber (NR)',
						'Polyethylene (PE)'
						]
			processes = ['Select Manufacturing Process',
						'Casting', 
						'Machining'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)


		elif part == 'Chain':
			minimize =  'Price'
			maximize = 'Fatigue Strength at 10^7 Cycles'
			materials = ['Select Material',
						'Medium carbon steel',
						'Low carbon steel',
						'Low alloy steel',
						'Cast iron - gray',
						'Cast iron - ductile (nodular)'
						]
			processes = ['Select Manufacturing Process',
						'Forming', 
						'Drawing', 
						'Machining',
						'Heat Treatment',
						'Joining',
						'Surface Treatment'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)


		elif part == 'Seat Post':
			minimize =  'Weight (Density)'
			maximize = 'Compressive Strength'
			materials = ['Select Material',
						'Cast Al-Alloys',
						'Low carbon steel',
						'Stainless Steel Cast',
						'Magnesium Alloys',
						'Low Alloy Steel'
						]
			processes = ['Select Manufacturing Process',
						'Forming',
						'Heat Treatment',
						'Joining',
						'Surface Treatment'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)


		elif part == 'Seat':
			minimize =  'Weight (Density)'
			maximize = 'Price'
			materials = ['Select Material',
						'Polyurethane',
						'Rigid Polymer',
						'Foam (HD)',
						'Rigid Polymer Foam (LD)',
						'Flexible Polymer Foam (VLD)',
						'Ceramic Foam'
						]
			processes = ['Select Manufacturing Process',
						'Injection molding',
						'Open Die Forging',
						'Casting'
						]
			material, process, material_just, process_just = make_selections(materials, processes, minimize, maximize)

		st.text("")
		st.text("")
		st.write(
			"""
			These are your selections. To make a change, go up :point_up:, select the part and 
			continue the process.
			""")

		if st.button('Reset Table', key=-1):
			try:
				os.system(ss.filepath+'rm parts_selction.csv')
				os.system(ss.filepath+'rm parts_material_process_justification.csv')
			except:
				pass
		else:
			try:
				selection_df.loc[len(selection_df)] = [part, material, process]
				selection_df = selection_df.drop_duplicates(subset=['Part'], keep='last')
				selection_df.index = range(1, len(selection_df)+1)
				selection_df.to_csv(ss.filepath+'parts_selction.csv', index=False)
				st.dataframe(selection_df, width=4000)

				justification_df.loc[len(justification_df)] = [part, material_just, process_just]
				justification_df = justification_df.drop_duplicates(subset=['Part'], keep='last')
				justification_df.index = range(1, len(justification_df)+1)
				justification_df.to_csv(ss.filepath+'parts_material_process_justification.csv', index=False)
				st.dataframe(justification_df, width=4000)

				#since the dataframes must exist, they are submitted here if group_state indicates that they should be
				group_state = group.load(ss.group_state.get('group_key'))
				if(group_state['roles_reported'][1] == False):
					submit_report_info(selection_df, justification_df, group_state)
			except:
				pass

def feedback():
	# writing
	st.header("Feedback **:red[TO]**")
	text = ""
	if path.isfile(ss.filepath+'fb_m_d.txt'):
		with open(ss.filepath+'fb_m_d.txt', 'r') as f:
			text = f.read()

	with st.form("mech_des_feedback"):
		fb_m_d = st.text_area("Your feedback to the Design Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_m_d != ""):
			with open(ss.filepath+"fb_m_d.txt", "w") as f:
				f.write(fb_m_d)
			st.experimental_rerun() #causes the submit button to only need to be pressed once
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_m_d.txt'):
				os.remove(ss.filepath+'fb_m_d.txt')
			st.experimental_rerun() #causes the submit button to only need to be pressed once
	
	text = ""
	if path.isfile(ss.filepath+'fb_m_i.txt'):
		with open(ss.filepath+'fb_m_i.txt', 'r') as f:
			text = f.read()

	with st.form("mech_ind_feedback"):
		fb_m_i = st.text_area("Your feedback to the Industrial Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_m_i != ""):
			with open(ss.filepath+"fb_m_i.txt", "w") as f:
				f.write(fb_m_i)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_m_i.txt'):
				os.remove(ss.filepath+'fb_m_i.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_m_pm.txt'):
		with open(ss.filepath+'fb_m_pm.txt', 'r') as f:
			text = f.read()

	with st.form("mech_proj_feedback"):
		fb_m_pm = st.text_area("Your feedback to the Project Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_m_pm != ""):
			with open(ss.filepath+"fb_m_pm.txt", "w") as f:
				f.write(fb_m_pm)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_m_pm.txt'):
				os.remove(ss.filepath+'fb_m_pm.txt')
			st.experimental_rerun()
			
	text = ""
	if path.isfile(ss.filepath+'fb_m_pum.txt'):
		with open(ss.filepath+'fb_m_pum.txt', 'r') as f:
			text = f.read()

	with st.form("mech_pur_feedback"):
		fb_m_pum = st.text_area("Your feedback to the Purchasing Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_m_pum != ""):
			with open(ss.filepath+"fb_m_pum.txt", "w") as f:
				f.write(fb_m_pum)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_m_pum.txt'):
				os.remove(ss.filepath+'fb_m_pum.txt')
			st.experimental_rerun()
	
	# reading
	st.header("Feedback **:red[From]**")
	st.markdown("---")
	if path.isfile(ss.filepath+'fb_d_m.txt'):
		st.write("Feedback from the **:red[Design Engineer]**:")
		with open(ss.filepath+'fb_d_m.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_i_m.txt'):
		st.write("Feedback from the **:red[Industrial Engineer]**:")
		with open(ss.filepath+'fb_i_m.txt', 'r') as f:
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

def submit_report_info(selection_df, justification_df, group_state):
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
		with open(ss.filepath+'fb_m_d.txt', 'r') as f:
			fb_m_d = f.read()

		with open(ss.filepath+'fb_m_i.txt', 'r') as f:
			fb_m_i = f.read()
		
		with open(ss.filepath+'fb_m_pm.txt', 'r') as f:
			fb_m_pm = f.read()

		with open(ss.filepath+'fb_m_pum.txt', 'r') as f:
			fb_m_pum = f.read()
			
	except FileNotFoundError:
		pass
	except:
		print('An error occurred')

	with open(ss.filepath+'report/'+ 'MechanicalEngineer' + '.txt', 'w') as f:
		f.write(ss.group + ': Mechanical Engineer: '+ ss.name +'\n')
		f.write(str(elapsed_time) + " Time Elapsed: " + str(elapsed_minutes) +" minutes and " + str(elapsed_seconds) + " seconds.\n")
		f.write(selection_df.to_string(index=False, justify='center') + '\n\n' + justification_df.to_string(index=False, justify='center'))
		f.write('\n' + '\n' + 'Feedback to the Design Engineer: '+ fb_m_d + '\n' +
				'Feedback to the Indistrial Engineer: '+ fb_m_i + '\n' +
				'Feedback to the Project Manager: '+ fb_m_pm + '\n' +
				'Feedback to the Purchasing Manager: '+ fb_m_pum)
	group_state['roles_reported'][1] = True
	group.save_group_state(group_state)
	print("Mechanical Enginner submitted the report successfully")

def display_m_e_code():	
	player_rejoin.render()
	st.button("CONTINUE", on_click=code_written_switch)

def code_written_switch():
	if ss.code_written:
		ss.code_written = False
	else:
		ss.code_written = True