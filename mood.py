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
    if not records:
        return pd.DataFrame() 

    df = pd.DataFrame(records)
    expected_columns = {'Timestamp', 'Mood', 'Note'}  
    if not expected_columns.issubset(df.columns):
        st.warning("Expected columns are missing from the sheet.")
        return pd.DataFrame()

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df.dropna(subset=['Timestamp'], inplace=True)
    df['Date'] = df['Timestamp'].dt.date
    df['Mood'] = df['Mood'].astype(str).str.strip().str.replace('\ufe0f', '', regex=True)
    return df

def plot_mood_chart(df, date, title):
    if df.empty or 'Date' not in df.columns or 'Mood' not in df.columns:
        st.info("No data available to plot.")
        return

    df_filtered = df[df['Date'] == date]
    if not df_filtered.empty:
        mood_counts = df_filtered['Mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']
        fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood', title=title)
        st.plotly_chart(fig)
    else:
        st.info(f"No moods logged on {date}.")

st.set_page_config(page_title="Mood Tracker", page_icon="🧠", layout="centered")
# Automatically refresh the dashboard every 30 seconds
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30 * 1000, key="auto_refresh")
except Exception:
    # If the autorefresh helper isn't available, continue without it
    pass
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
