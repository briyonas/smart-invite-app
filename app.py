import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# === GOOGLE SHEETS SETUP ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
creds_dict = st.secrets["gspread"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)

client = gspread.authorize(creds)
sheet = client.open("InvitationData").sheet1

# === TITLE ===
st.title("🎉 Smart Invitation Management System")
st.write("Enter guest details and get AI-assisted RSVP prediction & categorization.")

# === FORM ===
with st.form("invite_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    relationship = st.text_input("Relationship (e.g., Uncle, Manager, Friend)")
    rsvp = st.selectbox("RSVP Response", ["Yes", "No", "Maybe", "Not Responded"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        # === Category Logic ===
        relationship_lower = relationship.lower()
        if "uncle" in relationship_lower or "aunt" in relationship_lower or "cousin" in relationship_lower:
            category = "Family"
        elif "manager" in relationship_lower or "boss" in relationship_lower or "team" in relationship_lower:
            category = "Colleague"
        else:
            category = "Friend"

        # === RSVP Prediction Logic ===
        if category == "Family":
            predicted_rsvp = "Yes"
        elif category == "Friend":
            predicted_rsvp = "Maybe"
        else:
            predicted_rsvp = "No"

        # === Store to Google Sheet ===
        sheet.append_row([name, email, relationship, category, rsvp, predicted_rsvp])
        st.success(f"Guest '{name}' added with predicted RSVP: {predicted_rsvp}")

# === DASHBOARD ===
st.subheader("📊 Guest Dashboard")

# Load all data
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    st.write("### Overview")
    st.write(df)

    st.write("### RSVP Count")
    st.bar_chart(df["RSVP"].value_counts())

    st.write("### Category Breakdown")
    st.bar_chart(df["Category"].value_counts())
else:
    st.warning("No guests added yet.")
