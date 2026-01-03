import streamlit as st
import os

st.set_page_config(page_title="Hospital Login", layout="centered")

# -------- SESSION STATE --------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -------- UI --------
st.title("🏥 Hospital Dashboard Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not username and not password :
        st.error("please enter username and password")
    elif not username :
        st.error("please enter username")
    elif not password :
        st.error("please enter password")
    elif (username == os.environ.get("USERNAME") and password == os.environ.get("PASSWORD")):
        st.session_state.authenticated = True
        st.success("Login successful ✅")
        st.switch_page("pages/hospital_st.py")
    else:
        st.error("Invalid username or password ❌")

