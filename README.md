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

### 2. Google Sheets set-up

 - https://console.cloud.google.com/welcome?inv=1&invt=AbxfdA&project=mochiproj
