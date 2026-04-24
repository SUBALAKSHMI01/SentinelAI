import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# 🌟 Page Config
st.set_page_config(page_title="SentinelAI", page_icon="🔐", layout="wide")

# 🎨 Title Section
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🔐 SentinelAI</h1>
    <h4 style='text-align: center;'>Secure Prompt Analyzer with Audit Tracking</h4>
    <hr>
""", unsafe_allow_html=True)

# 📌 Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Analyze Prompt", "Audit Logs"])

# =========================================
# 🧠 ANALYZE PAGE
# =========================================
if page == "Analyze Prompt":

    st.subheader("🧠 Analyze Your Prompt")

    text = st.text_area("Enter your prompt", height=150)

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox("Select Role", ["employee", "admin"])

    with col2:
        user_id = st.text_input("Enter User ID")

    if st.button("Analyze 🚀"):

        if not text or not user_id:
            st.warning("Please enter both prompt and user ID")
        else:
            response = requests.post(
                f"{API_URL}/analyze",
                json={
                    "text": text,
                    "role": role,
                    "user_id": user_id
                }
            )

            data = response.json()

            st.success("Analysis Complete ✅")

            st.subheader("🔍 Detected Data")
            st.json(data["detected"])

            st.subheader("🔐 Masked Text")
            st.code(data["masked_text"])

            st.subheader("🔄 Final Output")
            st.code(data["final_response"])


# =========================================
# 📊 AUDIT LOGS PAGE (WITH LOGIN)
# =========================================
elif page == "Audit Logs":

    st.subheader("🔑 Audit Log Access")

    role = st.selectbox("Select Role", ["admin", "employee"])
    user_id = st.text_input("Enter User ID")

    if st.button("Login & View Logs"):

        if not user_id:
            st.warning("Please enter user ID")
        else:
            params = {
                "role": role,
                "user_id": user_id
            }

            response = requests.get(f"{API_URL}/logs", params=params)
            logs = response.json()

            if not logs:
                st.warning("No logs found")
            else:
                st.success("Logs fetched successfully ✅")

                for log in reversed(logs):
                    with st.expander(f"🧾 {log['timestamp']} | {log['user_id']}"):
                        st.write("**Role:**", log["role"])
                        st.write("**Original:**", log["original"])
                        st.write("**Masked:**", log["masked"])
                        st.write("**Detected:**")
                        st.json(log["detected"])