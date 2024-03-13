import streamlit as st

def Tab_Format():
	st.markdown("""
			<style>
				button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  					font-size: 20px;
  					color: #003040;
			   		font-weight: bold;
				}
				.stTabs [data-baseweb="tab-list"] {
					gap: 15px;
				}

				.stTabs [data-baseweb="tab"] {
					height: 45px;
					white-space: pre-wrap;
					background-color: #F0F2F6;
			   		border: 1px solid #003040;
					border-radius: 15px;
					gap: 25px;
					padding-top: 30px;
					padding-bottom: 30px;
				}

				.stTabs [aria-selected="true"] {
  					background-color: #5f9ea0;
				}

			</style>""", unsafe_allow_html=True)
	
def Button_Format():
	st.markdown("""
	<style>
	div.stButton > button:first-child {
    	border: 5px solid #5f9ea0;
    	color: white;
    	font-size: 20px;
    	border-radius: 10px 10px 10px 10px;
		background-color: #5f9ea0;
	}
	</style>
	""", unsafe_allow_html=True)

def downlad_format():
	st.markdown("""
	<style>
	[data-testid="stDownloadButton"] {
    	border: 5px solid #5f9ea0;
    	color: white;
    	font-size: 20px;
    	border-radius: 10px 10px 10px 10px;
		background-color: #5f9ea0;
	}
	</style>
	""", unsafe_allow_html=True)