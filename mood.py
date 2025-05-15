import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


sheets = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = "mochiproj-86bc0bb38ada.json"
sheet_name = "Mood Tracker"

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, sheets)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def append_entry(mood, note):
    sheet = get_sheet()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])

def load_data():
    sheet = get_sheet()
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    if not df.empty:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Date'] = df['Timestamp'].dt.date
        df['Mood'] = df['Mood'].str.strip().str.replace('\ufe0f', '', regex=True)  # Normalize emojis
    return df

def plot_mood_chart(df, date, title):
    df_filtered = df[df['Date'] == date]
    if not df_filtered.empty:
        mood_counts = df_filtered['Mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']
        fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood', title=title)
        st.plotly_chart(fig)
    else:
        st.info(f"No moods logged on {date}.")

st.set_page_config(page_title="Mood Tracker", page_icon="🧠", layout="centered")
st.experimental_rerun_interval = 30
st.title("🧠 Mood of the Queue")

st.subheader("Log a Mood")
mood = st.selectbox("Select your mood:", ["😊", "😠", "😕", "🎉", "🤬", "🙄"], index=0)
note = st.text_input("Optional note")
if st.button("Submit"):
    append_entry(mood, note)
    st.success("Mood logged!")

df = load_data()

st.subheader("📊 Mood Visualization (Today)")
today = datetime.today().date()
plot_mood_chart(df, today, "Today's Mood Counts")

st.subheader("📅 Filter Mood Entries by Date")
date_selected = st.date_input("Select a date", today)
plot_mood_chart(df, date_selected, f"Moods on {date_selected}")
