# Mood Tracker

This is a tool helps workers log and visualize the emotional “vibe” of the ticket queue throughout the day.

Built with **Streamlit**, it connects to **Google Sheets** for data storage and uses **Plotly** for interactive mood visualizations.

---

## Features

- Log a mood using emoji buttons
- Add optional notes (e.g., "Lots of Rx delays today")
- View mood trends for **today** or filter by any **past date**
- Auto-refreshing bar charts powered by Plotly
- ☁Google Sheets integration for real-time cloud logging

---

## 🚀 Getting Started

### 1. Clone the repo and install requirements

```bash
git clone https://github.com/your-username/mood-tracker.git
cd mood-tracker
pip install -r requirements.txt
```

### 2. Google Sheets set-up

 - Go to Google Cloud Console
 - Create a project and enable Google Sheets API and Google Drive API
 - Create a Service Account and download the credentials.json file
 - Create a Google Sheet with columns : Timestamp | Mood | Note
 - Share the sheet with your service account
 - Replace credentials and sheet_name in mood.py with your respective values


### 3. Run the app
```bash
streamlit run mood_tracker.py
```


