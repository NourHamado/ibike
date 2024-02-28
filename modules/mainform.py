import streamlit as st
from .form0 import form_0
from .form1 import form_1
from .form2 import form_2
from .form3 import form_3
from .form4 import form_4
from .form5 import form_5
from .form6 import form_6
from .form7 import form_7
from .form8 import form_8
from .form9 import form_9
from .form10 import form_10
from .form11 import form_11
from .form12 import form_12
from .form13 import form_13

def main_form():
    if "form_statuses" not in st.session_state:
        st.session_state.form_statuses = {
            "form0": False,
            "form1": False,
            "form2": False,
            "form3": False,
            "form4": False,
            "form5": False,
            "form6": False,
            "form7": False,
            "form8": False,
            "form9": False,
            "form10": False,
            "form11": False,
            "form12": False,
            "form13": False,
        }
    
    form_names = {
        "form0": "Starting Form",
        "form1": "Consent Form",
        "form2": "Basic Information Form",
        "form3": "Manufacturing Knowledge Form",
        "form4": "Defining Manufacturing Terms Form",
        "form5": "YouTube Video 1 Form",
        "form6": "Level of Agreement Form",
        "form7": "iBike Part 1 Form",
        "form8": "YouTube Video 2 Form",
        "form9": "iBike Part 2 Form",
        "form10": "YouTube Video 3 Form",
        "form11": "iBike Part 3 Form",
        "form12": "Manufacturing Form",
        "form13": "Ending Form",
    }
    st.sidebar.header("Please read the form carefully and fill in the below form.")
    form_statuses = st.session_state.form_statuses
    user_selected_page = st.sidebar.radio("Select a form", list(form_statuses.keys()), format_func=lambda x: form_names[x])

    # Forms to exclude from status bar updates
    forms_to_exclude = ["form0", "form3", "form5", "form8", "form10", "form13"]
    if user_selected_page == "form0":
        form_0()
    elif user_selected_page == "form1":
        if form_1():
            form_statuses["form1"] = True  
    elif user_selected_page == "form2":
        if form_2():
            form_statuses["form2"] = True 
    elif user_selected_page == "form3":
        form_3()
    elif user_selected_page == "form4":
        if form_4():
            form_statuses["form4"] = True  
    elif user_selected_page == "form5":
        form_5()
    elif user_selected_page == "form6":
        if form_6():
            form_statuses["form6"] = True  
    elif user_selected_page == "form7":
        if form_7():
            form_statuses["form7"] = True  
    elif user_selected_page == "form8":
        form_8()
    elif user_selected_page == "form9":
        if form_9():
            form_statuses["form9"] = True 
    elif user_selected_page == "form10":
        form_10()
    elif user_selected_page == "form11":
        if form_11():
            form_statuses["form11"] = True  
    elif user_selected_page == "form12":
        if form_12():
            form_statuses["form12"] = True 
    elif user_selected_page == "form13":
        form_13()
    st.sidebar.header("Form Completion Status")
    for page, completed in form_statuses.items():
        if page not in forms_to_exclude:
            form_name = form_names[page]
            if completed:
                st.sidebar.write(f"{form_name}: ✔️")
            else:
                st.sidebar.write(f"{form_name}: ❌")

if __name__ == "__main__":
    main_form()
