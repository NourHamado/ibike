import streamlit as st
import numpy as np
import sympy as sp
import time
import decimal
import matplotlib.pyplot as plt
from streamlit import session_state as ss
from modules import group, player, game, rejoin
from PIL import Image, ImageDraw, ImageFont
import os
from os import path

def render():

	st.set_option('deprecation.showPyplotGlobalUse', False)
	st.title('Design Engineer')
	
	st.write("Welcome to the Design Engineer Page!")

	st.markdown(
		"""
		Your role revolves around selecting the design parameters of the bike so as to maximize its stability. You
		will be provided with the set of the parameters with brief description.
		""")
	
	st.markdown('---')

	st.image('files/images/design_eng_1.png')
	st.markdown('---')
	st.image('files/images/design_eng_2.png')
	st.markdown('---')
	#st.image('design_eng_3.png')
	#st.markdown('---')

	# Input parameters

	# w = st.slider('Insert Wheel base (m)', min_value=0.8, max_value=1.2, value=0.8, step=0.01)

	player.display_current_orders()

	st.markdown('---')

	col1, col2 = st.columns([1, 2])

	with col1:
		w = st.slider('Insert Wheel base (m)', min_value=0.8, max_value=1.2, value=0.8, step=0.01)
		mB = st.slider('Mass of Rear Frame and Rider (kg)', min_value=50, max_value=100, value=50)
		rF = st.slider('Front Wheel Radius (m)', min_value=0.3, max_value=0.4, value=0.3, step=0.01)
		rR = st.slider('Rear Wheel Radius (m)', min_value=0.3, max_value=0.4, value=0.3, step=0.01)
		ss.design_parameters = np.array([w, mB, rF, rR])

	c=0.08; # Trail (m)
	lamda=np.pi/10; # Steer axis tilt (rad)
	g=9.81; # Gravitational acceleration (N/kg or m/s)
	#v=zeros(100,1);# Forward velocity of bicycle (m/s)
	# Rear wheel, R

	# rR = st.slider('Rear Wheel Radius (m)', min_value=0.3, max_value=0.4, value=0.3, step=0.01)

	mR=2; # Mass of Rear Frame and Rider (kg)
	IRxx=0.0603; # Mass moments of inertia (kg m^2) 
	IRyy=0.0603; # Mass moments of inertia (kg m^2)
	# Read body and frame assembly, B
	xB=0.3; # Position of center of mass (m)
	zB=-0.9; # Position of center of mass (m)

	# mB = st.slider('Mass of Rear Frame and Rider (kg)', min_value=50, max_value=100, value=50)

	IBxx=9.2; # Mass moment of inertia (kg m^2)
	IByy=11; # Mass moment of inertia (kg m^2)
	IBzz=2.8; # Mass moment of inertia (kg m^2)
	IBxz=0; # Mass moment of inertia (kg m^2)
	# Front handlebar and fork assembly, H
	xH=0.91; # Position of center of mass (m)
	zH=-0.68; # Position of center of mass (m)
	mH=4; # Mass of Rear Frame and Rider (kg)
	IHxx=0.05892; # Mass moment of inertia (kg m^2)
	IHyy=0.12; # Mass moment of inertia (kg m^2)
	IHzz=0.00708; # Mass moment of inertia (kg m^2)
	IHxz=0; # Mass moment of inertia (kg m^2)
	# Front wheel, F

	# rF = st.slider('Front Wheel Radius (m)', min_value=0.3, max_value=0.4, value=0.3, step=0.01)


	mF=3; # Mass of Rear Frame and Rider (kg)
	IFxx=0.1405; # Mass moments of inertia (kg m^2) 
	IFyy=0.1405; # Mass moments of inertia (kg m^2)

	# Calculation
	# Total mass and center of mass location with respect to rear contact point p 

	mT=mR+mB+mH+mF; # B 1
	xT=(xB*mB+xH*mH+w*mF)/mT; # B 2
	zT=(-rR*mR+zB*mB+zH*mH-rF*mF)/mT; # B 3 
	# Relevant mass moments and products of inertia with respect to rear contact point P
	ITxx=IRxx+IBxx+IHxx+IFxx+mR*rR**2+mB*zB**2+mH*zH**2+mF*rF**2; # B 4
	ITxz=IBxz+IHxz-mB*xB*zB-mH*xH*zH+mF*w*rF; # B 5
	IRzz=IRxx; IFzz=IFxx; # B 6
	ITzz=IRzz+IBzz+IHzz+IFzz+mB*xB**2+mH*xH**2+mF*w**2; # B 7
	# Total mass, center of location, and mass moment of inertia with respect to rear contact point P
	mA=mH+mF; # B 8
	xA=(xH*mH+w*mF)/mA; zA=(zH*mH-rF*mF)/mA; # B 9
	IAxx=IHxx+IFxx+mH*(zH-zA)**2+mF*(rF+zA)**2; # B 10
	IAxz=IHxz-mH*(xH-xA)*(zH-zA)+mF*(w-xA)*(rF+zA); # B 11
	IAzz=IHzz+IFzz+mH*(xH-xA)**2+mF*(w-xA)**2; # B 12
	# The center of mass of the front assembly form the center of mass of front wheel
	uA=(xA-w-c)*np.cos(lamda)-zA*np.sin(lamda); # B 13
	# Three special inertia quantities
	IAll=mA*uA**2+IAxx*(np.sin(lamda))**2+2*IAxz*np.sin(lamda)*np.cos(lamda)+IAzz*(np.cos(lamda))**2; # A 14
	IAlx=-mA*uA*zA+IAxx*np.sin(lamda)+IAxz*np.cos(lamda); # B 15
	IAlz=mA*uA*xA+IAxz*np.sin(lamda)+IAzz*np.cos(lamda); # B 16
	# The ratio of mechanical trail
	nu=(c/w)*np.cos(lamda); # B 17
	# Gyroscopic coefficients
	SR=IRyy/rR; SF=IFyy/rF; ST=SR+SF; # B 18
	SA=mA*uA+nu*mT*xT; # B 19
	# Mass Matrix, M
	M=np.zeros((2, 2));
	M[0,0]=ITxx; M[0,1]=IAlx+nu*ITxz; M[1,0]=M[0,1]; 
	M[1,1]=IAll+2*nu*IAlz+nu**2*ITzz; # A 20

	# Gravity-dependent stiffness matrix, Ko
	Ko=np.zeros((2, 2));
	Ko[0,0]=mT*zT; Ko[0,1]=-SA; Ko[1,0]=Ko[0,1]; Ko[1,1]=-SA*np.sin(lamda); # B 22

	# Velocity-dependent stiffness matrix, K2
	K2=np.zeros((2, 2));
	K2[0,0]=0; K2[0,1]=((ST-mT*zT)/w)*np.cos(lamda); K2[1,0]=0; 
	K2[1,1]=((SA+SF*np.sin(lamda))/w)*np.cos(lamda); # A 24

	# Damping-like matrix, C
	C=np.zeros((2, 2));
	C[0,0]=0; C[0,1]=nu*ST+SF*np.cos(lamda)+(ITxz/w)*np.cos(lamda)-nu*mT*zT; 
	C[1,0]=-(nu*ST+SF*np.cos(lamda)); 
	C[1,1]=(IAlz/w)*np.cos(lamda)+nu*(SA+(ITzz/w)*np.cos(lamda)); # B 26

	########################################################
	# Finding eigenvalues
	v = sp.symbols('v', real=True)
	sigma = sp.symbols('sigma', real=True)
	EOM=M*sigma**2+v*C*sigma+g*Ko+v**2*K2;
	EOM = sp.Matrix(EOM)
	d = EOM.det()
	s=sp.solveset(d, sigma)
	vel=np.zeros((100,1));
	sol=np.zeros((100,4), dtype=complex);
	for i in range (1, 101):
		vel[i-1,0] = i/10;
		aa = s.subs(v, i/10) 
		sol[i-1,:] = np.fromiter(aa, dtype=complex)

	real_sol=np.real(sol)
	real_sol_index=np.where(np.sum(real_sol < 0, axis=1) == 4)[0]
	########################################################
	with col2:
		st.markdown('**:red[To obtain a better solution, increase the gap between the two vertical dashed lines.]**')
		solution_graph = plt.figure(figsize=(12, 12))
		plt.plot(vel, real_sol, linewidth=2)
		plt.plot(vel[real_sol_index[0]]*np.ones((len(vel),1)), np.linspace(-30, 11,len(vel)), linestyle='--', linewidth=3)
		plt.plot(vel[real_sol_index[-1]]*np.ones((len(vel),1)), np.linspace(-30, 11,len(vel)), linestyle='--', linewidth=3)
		plt.title('Solution roots vs. velocity diagram of the standard model', fontsize=20)
		plt.xlabel('Velocity (m/s)', fontsize=20)
		plt.ylabel('Real part of the Solution roots', fontsize=20)
		plt.grid(linestyle='-.')

		#checking if report is needed, since pyplot will clear the graph we need to send
		group_state = group.load(ss.group_state.get('group_key'))
		if(group_state['roles_reported'][0] == False):
			submit_report_info(solution_graph, group_state)
			
		st.pyplot()
	
	plt.figure(figsize=(12, 8))
	h = int(1024*(8/12))
	w_ = 1024
	img = Image.new('RGB', (w_, h), (255, 255, 255))
	draw = ImageDraw.Draw(img)
	font_size = 24  # Choose the desired font size
	font = ImageFont.truetype("files/fonts/Arial.ttf", font_size)

	radius_1 = int((rR / 0.4) * 100)
	center_coordinates_1 = (200, h - radius_1 - 100)

	length = int((w / 1.2) * 500)
	radius_2 = int((rF / 0.4) * 100)
	center_coordinates_2 = (200 + length, h - radius_2 - 100)
	color = (0, 0, 0)
	thickness = 2

	#####################################
	pt3 = center_coordinates_1[0] - radius_1
	pt4 = center_coordinates_1[1]
	draw.line([center_coordinates_1, (pt3, pt4)], fill=(255, 0, 0), width=2)

	bottomLeftCornerOfText = center_coordinates_1[0] - 60, center_coordinates_1[1] + 20
	draw.text(bottomLeftCornerOfText, f'R (RW) = {rR} m', font=font, fill=(0, 0, 0))

	draw.ellipse([(center_coordinates_1[0] - radius_1, center_coordinates_1[1] - radius_1), (center_coordinates_1[0] + radius_1, center_coordinates_1[1] + radius_1)], outline=color, width=thickness)

	#####################################
	pt3 = center_coordinates_2[0] - radius_2
	pt4 = center_coordinates_2[1]
	draw.line([center_coordinates_2, (pt3, pt4)], fill=(255, 0, 0), width=2)

	bottomLeftCornerOfText = center_coordinates_2[0] - 60, center_coordinates_2[1] + 20
	draw.text(bottomLeftCornerOfText, f'R (FW) = {rF} m', font=font, fill=(0, 0, 0))

	draw.ellipse([(center_coordinates_2[0] - radius_2, center_coordinates_2[1] - radius_2), (center_coordinates_2[0] + radius_2, center_coordinates_2[1] + radius_2)], 		outline=color, width=thickness)

	#####################################
	pt1 = center_coordinates_1[0]
	pt2 = center_coordinates_1[1] + radius_1 + 20

	pt3 = center_coordinates_2[0]
	pt4 = center_coordinates_2[1] + radius_2 + 20
	draw.line([(pt1, pt2), (pt3, pt4)], fill=(255, 0, 0), width=2)

	bottomLeftCornerOfText = (int((pt1 + pt2) / 3), pt2 + 25)
	draw.text(bottomLeftCornerOfText, f'Wheel base = {w} m', font=font, fill=(0, 0, 0))

	#####################################

	offset = int(np.sin(np.pi / 10) * (center_coordinates_2[1] - int(3 * radius_2)))

	head = (center_coordinates_2[0] - offset, center_coordinates_2[1] - int(3 * radius_2))
	draw.line([center_coordinates_2, head], fill=color, width=thickness)

	draw.line([head, center_coordinates_1], fill=color, width=thickness)

	head2 = head[0] - 100, head[1]
	draw.line([head, head2], fill=color, width=thickness)

	#####################################
	center_coordinates_2 = head[0] - 150, head[1]
	draw.ellipse([(center_coordinates_2[0] - int(mB * 20 / 50), center_coordinates_2[1] - int(mB * 20 / 50)), (center_coordinates_2[0] + int(mB * 20 / 50), center_coordinates_2[1] + int(mB * 20 / 50))], fill=(255, 0, 0))

	pt1, pt2 = center_coordinates_2[0] - 50, center_coordinates_2[1] - (int(mB * 20 / 50) + 10)
	bottomLeftCornerOfText = (pt1, pt2)
	draw.text(bottomLeftCornerOfText, f'Mass = {mB} kg', font=font, fill=(0, 0, 0))

	plt.imshow(img)
	plt.xticks([])
	plt.yticks([])
	plt.show()
	st.pyplot()
	
def feedback():
	# writing
	st.header("Feedback **:red[TO]**")

	text = ""
	if path.isfile(ss.filepath+'fb_d_m.txt'):
		with open(ss.filepath+'fb_d_m.txt', 'r') as f:
			text = f.read()

	with st.form("des_mech_feedback"):
		fb_d_m = st.text_area("Your feedback to the Mechanical Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_d_m != ""):
			with open(ss.filepath+"fb_d_m.txt", "w") as f:
				f.write(fb_d_m)
			st.experimental_rerun() #causes the submit button to only need to be pressed once
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_d_m.txt'):
				os.remove(ss.filepath+'fb_d_m.txt')
			fb_d_m = ""
			st.experimental_rerun() #causes the submit button to only need to be pressed once
	
	text = ""
	if path.isfile(ss.filepath+'fb_d_i.txt'):
		with open(ss.filepath+'fb_d_i.txt', 'r') as f:
			text = f.read()

	with st.form("des_ind_feedback"):
		fb_d_i = st.text_area("Your feedback to the Industrial Engineer:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_d_i != ""):
			with open(ss.filepath+"fb_d_i.txt", "w") as f:
				f.write(fb_d_i)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_d_i.txt'):
				os.remove(ss.filepath+'fb_d_i.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_d_pm.txt'):
		with open(ss.filepath+'fb_d_pm.txt', 'r') as f:
			text = f.read()
	
	with st.form("des_proj_feedback"):
		fb_d_pm = st.text_area("Your feedback to the Project Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_d_pm != ""):
			with open(ss.filepath+"fb_d_pm.txt", "w") as f:
				f.write(fb_d_pm)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_d_pm.txt'):
				os.remove(ss.filepath+'fb_d_pm.txt')
			st.experimental_rerun()
	
	text = ""
	if path.isfile(ss.filepath+'fb_d_pum.txt'):
		with open(ss.filepath+'fb_d_pum.txt', 'r') as f:
			text = f.read()
	
	with st.form("des_pur_feedback"):
		fb_d_pum = st.text_area("Your feedback to the Purchasing Manager:", text)
		col1, whitespace, col2 = st.columns((100, 400, 129))
		with col1:
			feedback_submission = st.form_submit_button("Submit")
		with whitespace:
			st.write("") #no content, this column is just to properly align the clear feedback button
		with col2:
			clear_submission = st.form_submit_button("Clear Feedback")
		
		if (feedback_submission and fb_d_pum != ""):
			with open(ss.filepath+"fb_d_pum.txt", "w") as f:
				f.write(fb_d_pum)
			st.experimental_rerun()
		elif (clear_submission):
			if path.isfile(ss.filepath+'fb_d_pum.txt'):
				os.remove(ss.filepath+'fb_d_pum.txt')
			st.experimental_rerun()

	# reading	
	st.header("Feedback **:red[From]**")
	st.markdown("---")
	if path.isfile(ss.filepath+'fb_m_d.txt'):		
		st.write("Feedback from the **:red[Mechanical Engineer]**:")
		with open(ss.filepath+'fb_m_d.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_i_d.txt'):
		st.write("Feedback from the **:red[Industrial Engineer]**:")
		with open(ss.filepath+'fb_i_d.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_pm_d.txt'):
		st.write("Feedback from the **:red[Project Manager]**:")
		with open(ss.filepath+'fb_pm_d.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

	if path.isfile(ss.filepath+'fb_pum_d.txt'):
		st.write("Feedback from the **:red[Purchasing Manager]**:")
		with open(ss.filepath+'fb_pum_d.txt', 'r') as f:
			text = f.read()
		st.write(text)
		st.markdown("---")

def submit_order_info(order_key):
	group_state = group.load(ss.group)
	group_state['orders'][order_key]['wheel_base'] = (str(ss.design_parameters[0]) + ' meters')
	group_state['orders'][order_key]['total_mass'] = (str(ss.design_parameters[1]) + ' kilograms')
	group_state['orders'][order_key]['front_wheel_rad'] = (str(ss.design_parameters[2]) + ' meters')
	group_state['orders'][order_key]['back_wheel_rad'] = (str(ss.design_parameters[3]) + ' meters')
	group.save_group_state(group_state)

def submit_report_info(fig, group_state):
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
		with open(ss.filepath+'fb_d_m.txt', 'r') as f:
			fb_d_m = f.read()
		with open(ss.filepath+'fb_d_i.txt', 'r') as f:
			fb_d_i = f.read()
		with open(ss.filepath+'fb_d_pm.txt', 'r') as f:
			fb_d_pm = f.read()
		with open(ss.filepath+'fb_d_pum.txt', 'r') as f:
			fb_d_pum = f.read()
	except FileNotFoundError:
		pass
		#print(f"One or more feedback files not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

	with open(ss.filepath+'report/'+ 'DesignEngineer' + '.txt', 'w') as f:
		f.write(ss.group + ': Design Engineer: '+ ss.name + '\n')
		f.write(str(elapsed_time) + " Time Elapsed: " + str(elapsed_minutes) +" minutes and " + str(elapsed_seconds) + " seconds.\n"
				'Wheel Base: ' + str(ss.design_parameters[0]) + '\n' +
				'Total Mass: ' + str(ss.design_parameters[1]) + '\n' +
				'Front Wheel Radius: '+ str(ss.design_parameters[2]) + '\n' +
				'Rear Wheel Radius: '+ str(ss.design_parameters[3]) + '\n' + '\n' +
				'Feedback to the Mechanical Engineer: '+ fb_d_m+ '\n' +
                'Feedback to the Indistrial Engineer: '+ fb_d_i + '\n' +
                'Feedback to the Project Manager: '+ ('N/A' if fb_d_pm is None else fb_d_pm) + '\n' +
                'Feedback to the Purchasing Manager: '+ fb_d_pum)
	fig.savefig(ss.filepath+'report/' + 'DesignEngineer' + '_graph.png')
	group_state['roles_reported'][0] = True
	group.save_group_state(group_state)
	print("Design Enginner submitted the report successfully")

