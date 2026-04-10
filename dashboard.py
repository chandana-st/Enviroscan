import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import smtplib
import folium
from email.mime.text import MIMEText
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import re
from openai import OpenAI
import requests
from streamlit_autorefresh import st_autorefresh
import docx2txt
import base64
from PyPDF2 import PdfReader

from rules import handle_rules

# ================= PAGE CONFIG =================
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")

# ================= PREMIUM CSS =================
st.markdown("""
<style>

/* ===== APP BACKGROUND ===== */
.stApp {
    background:
        linear-gradient(rgba(255,255,255,0.96), rgba(255,255,255,0.96)),
        url("https://images.unsplash.com/photo-1473773508845-188df298d2d1");
    background-size: cover;
    background-position: center;
}

/* ===== FIX ALL TEXT VISIBILITY ===== */
h1, h2, h3, h4, h5, h6, p, label, div {
    color: #0f172a !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown {
    color: #e2e8f0 !important;
}
/* ===== FIX HEADER (DEPLOY / STOP BUTTONS) ===== */
header[data-testid="stHeader"] {
    background: rgba(255,255,255,0.95) !important;
    border-bottom: 1px solid #e2e8f0 !important;
}

/* Make header text/icons visible */
header[data-testid="stHeader"] * {
    color: #0f172a !important;
}

/* Specifically target Deploy/Stop buttons */
header[data-testid="stHeader"] button {
    background: #ffffff !important;
    color: #0f172a !important;
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 4px 10px !important;
}

/* Hover effect */
header[data-testid="stHeader"] button:hover {
    background: #eff6ff !important;
    color: #2563eb !important;
}
/* ===== SAFE TEXT COLOR FIX ===== */
body, .stApp {
    color: #0f172a;
}

/* Fix DataFrame popup menus (3 dots menu) */
[data-baseweb="menu"],
[data-baseweb="popover"],
[data-baseweb="list"] {
    background: #ffffff !important;
    color: #0f172a !important;
}

/* Menu items */
[data-baseweb="menu"] *,
[data-baseweb="popover"] * {
    color: #0f172a !important;
}

/* Hover effect */
[data-baseweb="menu"] li:hover {
    background: #eff6ff !important;
    color: #2563eb !important;
}

/* ===== SIDEBAR SELECTBOX ===== */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: #0b1220 !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color: #ffffff !important;
    opacity: 1 !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stSelectbox input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stSelectbox input::placeholder {
    color: #cbd5e1 !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] .stSelectbox svg {
    fill: #ffffff !important;
}

/* ===== MAIN PAGE SELECTBOX ===== */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.78) !important;
    border: 1px solid rgba(37, 99, 235, 0.20) !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    color: #0f172a !important;
    box-shadow: none !important;
}

.stSelectbox div[data-baseweb="select"] div,
.stSelectbox div[data-baseweb="select"] span {
    color: #0f172a !important;
    opacity: 1 !important;
    background: transparent !important;
}

.stSelectbox input {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: transparent !important;
}

.stSelectbox input::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

.stSelectbox svg {
    fill: #0f172a !important;
}

/* ===== MAIN PAGE SELECTBOX FOCUS / ACTIVE ===== */
.stSelectbox div[data-baseweb="select"] > div:focus-within,
.stSelectbox div[data-baseweb="select"] > div:hover,
.stSelectbox div[data-baseweb="select"] > div:active {
    background: rgba(255,255,255,0.94) !important;
    border: 1px solid #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.12) !important;
}

/* ===== DROPDOWN ===== */
div[role="listbox"] {
    background: #ffffff !important;
    border: 1px solid #dbe4f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18) !important;
    z-index: 99999 !important;
}

ul[data-testid="stSelectboxVirtualDropdown"] {
    background: #ffffff !important;
}

ul[data-testid="stSelectboxVirtualDropdown"] li,
ul[data-testid="stSelectboxVirtualDropdown"] li * {
    background: #ffffff !important;
    color: #0f172a !important;
    opacity: 1 !important;
}

ul[data-testid="stSelectboxVirtualDropdown"] li:hover,
ul[data-testid="stSelectboxVirtualDropdown"] li:hover * {
    background: #eff6ff !important;
    color: #0f172a !important;
}

ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"],
ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] * {
    background: #dbeafe !important;
    color: #1d4ed8 !important;
    font-weight: 700 !important;
}

div[role="menu"],
div[role="listbox"],
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="select"] {
    background-color: #1f2937 !important;
    color: #f9fafb !important;
    border: 1px solid #374151 !important;
}

div[role="menu"] *,
div[role="listbox"] *,
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[data-baseweb="select"] * {
    color: #f9fafb !important;
}

div[role="menuitem"]:hover,
li:hover,
[data-baseweb="menu"] li:hover {
    background-color: #374151 !important;
    color: #ffffff !important;
}
section[data-testid="stFileUploadDropzone"] button {
    background-color: #4F46E5 !important; /* A nice indigo blue */
    color: white !important;
    border: 1px solid white !important;
    visibility: visible !important;
    }
    
/* This ensures the 'Drag and drop' text is also readable */
section[data-testid="stFileUploadDropzone"] label {
    color: white !important;
}

/* ===== TITLES ===== */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #0f172a !important;
}

.sub-title {
    text-align: center;
    font-size: 1.2rem;
    color: #334155 !important;
    margin-bottom: 20px;
}

/* ===== CARDS ===== */
.metric-box {
    background: white;
    padding: 1.2rem;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border-top: 5px solid #2563eb;
    transition: 0.3s;
}

.metric-box:hover {
    transform: translateY(-5px);
}

.glass-card {
    background: rgba(255,255,255,0.9);
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* ===== BUTTONS ===== */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
}

.stDownloadButton > button:hover,
.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    color: white !important;
}



/* ===== TABS ===== */
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: #334155 !important;
}

.stTabs [aria-selected="true"] {
    color: #2563eb !important;
    border-bottom: 3px solid #2563eb;
}

</style>
""", unsafe_allow_html=True)
# ================= HEADER =================
st.markdown('<div class="main-title">EnviroScan Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-Powered Air Pollution Monitoring & Prediction System</div>', unsafe_allow_html=True)

# ================= LOAD DATA =================
df = pd.read_csv("vij_hyd_labelled_dataset.csv")

model = joblib.load("models/gradient_boost_pollution_model.pkl")
le = joblib.load("models/label_encoder.pkl")

FEATURE_COLS = [
    "pm2_5","pm10","no2","o3","so2","co",
    "road_count","industrial_count","waste_count","farmland_count"
]

# ================= SIDEBAR =================
st.sidebar.markdown('<div class="sidebar-title">  Filters</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
location = st.sidebar.selectbox(
    "Select Location",
    sorted(df["location"].unique())
)

pollutant = st.sidebar.selectbox(
    "Select Pollutant",
    ["pm2_5","pm10","no2","o3","so2","co"]
)

filtered_df = df[df["location"] == location]

if filtered_df.empty:
    st.warning("No data available")
    st.stop()

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Dashboard", 
    " Map", 
    " Reports",
    " Chatbot",
    " Live pollution detection"
])


import time

def animated_kpi(label, value, suffix=""):
    placeholder = st.empty()

    for i in range(0, 101, 5):
        display_val = (value * i) / 100
        placeholder.markdown(f"""
        <div class="metric-box">
            <div style="font-size:32px; font-weight:800;">
                {display_val:.2f}{suffix}
            </div>
            <div style="font-size:14px; color:#475569;">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.01)

    placeholder.markdown(f"""
    <div class="metric-box">
        <div style="font-size:32px; font-weight:800;">
            {value:.2f}{suffix}
        </div>
        <div style="font-size:14px; color:#475569;">
            {label}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= GLOBAL BACKGROUND FUNCTION =================

with tab1:

    st.subheader(" Pollution Indicators")

    # ✅ DEFINE COLUMNS HERE (IMPORTANT FIX)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        animated_kpi("PM2.5", filtered_df["pm2_5"].mean())

    with col2:
        animated_kpi("PM10", filtered_df["pm10"].mean())

    with col3:
        animated_kpi("NO2", filtered_df["no2"].mean())

    with col4:
        animated_kpi("O3", filtered_df["o3"].mean())

    with col5:
        animated_kpi("SO2", filtered_df["so2"].mean())

    with col6:
        animated_kpi("CO", filtered_df["co"].mean())

    st.markdown('</div>', unsafe_allow_html=True)

    # AQI
    st.subheader(" Air Quality Index (AQI)")

    def get_aqi_category(pm25):
        if pm25 <= 0.15: return "Good "
        elif pm25 <= 0.25: return "Moderate "
        elif pm25 <= 0.50: return "Unhealthy "
        elif pm25 <= 0.75: return "Poor "
        else: return "Hazardous "

    avg_pm25 = filtered_df["pm2_5"].mean()
    aqi_status = get_aqi_category(avg_pm25)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#facc15,#f59e0b);
    padding:15px;border-radius:15px;color:white;text-align:center;">
     AQI Status: {aqi_status}
    </div>
    """, unsafe_allow_html=True)

    st.write(f"Average PM2.5: {avg_pm25:.2f}")

    # HEALTH
    def health_advice(pm25):
        if pm25 <= 0.15:
            return "✅ Good air quality "
        elif pm25 <= 0.25:
            return "Sensitive individuals should reduce prolonged outdoor exertion"
        elif pm25 <= 0.50:
            return "Wear N95 mask and limit outdoor activities "
        elif pm25 <= 0.75:
            return "Very Unhealthy. Stay indoors, use air purifiers, and avoid physical exertion "
        else:
            return "Hazardous! Stay indoors "

    st.subheader(" Health Recommendations")
    st.markdown(f"""
    <div style="background:#10b981;color:white;padding:15px;border-radius:15px;">
    {health_advice(avg_pm25)}
    </div>
    """, unsafe_allow_html=True)

    # SLIDERS
        # ================= SAFE SLIDER FUNCTION =================
    def safe_slider(label, series, is_int=False):
        min_val = series.min()
        max_val = series.max()
        mean_val = series.mean()

        # 🔥 FIX: if min == max → create range
        if min_val == max_val:
            min_val = min_val - 5
            max_val = max_val + 5

        if is_int:
            return st.slider(label, int(min_val), int(max_val), int(mean_val))
        else:
            return st.slider(label, float(min_val), float(max_val), float(mean_val))

    # ================= SLIDERS =================
    st.subheader(" Adjust Pollution Parameters")

    col1, col2 = st.columns(2)

    with col1:
        pm2_5 = safe_slider("PM2.5", filtered_df["pm2_5"])
        pm10 = safe_slider("PM10", filtered_df["pm10"])
        no2 = safe_slider("NO2", filtered_df["no2"])
        o3 = safe_slider("O3", filtered_df["o3"])
        so2 = safe_slider("SO2", filtered_df["so2"])
        co = safe_slider("CO", filtered_df["co"])

    with col2:
        road = safe_slider("Road Count", filtered_df["road_count"], True)
        industrial = safe_slider("Industrial Count", filtered_df["industrial_count"], True)
        waste = safe_slider("Waste Count", filtered_df["waste_count"], True)
        farm = safe_slider("Farmland Count", filtered_df["farmland_count"], True)

    # ================= PREDICTION =================
    st.subheader(" Predict Pollution Source")

    if st.button("Predict Source"):
        input_data = pd.DataFrame([[pm2_5, pm10, no2, o3, so2, co,
                                    road, industrial, waste, farm]],
                                  columns=FEATURE_COLS)

        pred = model.predict(input_data)
        proba = model.predict_proba(input_data)

        source = le.inverse_transform(pred)[0]
        confidence = max(proba[0]) * 100

        st.success(f"Predicted Source: {source}")
        st.info(f"Confidence: {confidence:.2f}%")


    # TABLE
    st.subheader(" Detailed Report")
    table_df = filtered_df.sort_values(by=pollutant, ascending=False)
    st.dataframe(table_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.subheader(" Download Report")

    csv = table_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{location}_pollution_report.csv",
        mime="text/csv"
    )
    
    #  EMAIL ALERT
    import smtplib
    from email.mime.text import MIMEText

# ---------- AQI LOGIC ----------
    def get_aqi_status(pm25):
        if pm25 <= 0.15:
            return "Good 🟢", "Air quality is good. Safe for outdoor activities."
        elif pm25 <= 0.25:
           return "Moderate 🟡", "Moderate air quality. Sensitive people should reduce outdoor exposure."
        elif pm25 <= 0.50:
           return "Unhealthy ⚠️", "Wear a mask and avoid prolonged outdoor exposure."
        else:
           return "Hazardous 🔴", "Stay indoors. Avoid outdoor activity completely."

# ---------- EMAIL BUTTON ----------
    st.subheader(" Send Email Alert")

    if st.button("Send Email Alert"):
        try:
            avg_pm25 = filtered_df["pm2_5"].mean()
            if pd.notna(avg_pm25):
                aqi_status, advice = get_aqi_status(avg_pm25)
                avg_pm25_text = f"{avg_pm25:.2f}"
            else:
                aqi_status, advice = "Unknown", "No sufficient data available."
                avg_pm25_text = "N/A"
            email_body = f"""
Pollution Alert for {location}

AQI Status: {aqi_status}
Average PM2.5: {avg_pm25_text}

Health Advice:
{advice}
"""
            msg = MIMEText(email_body)
            msg["Subject"] = "🚨 Pollution Alert"
            msg["From"] = "chandusst987@gmail.com"
            msg["To"] = "chandusst987@gmail.com"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

        # 🔴 IMPORTANT: USE APP PASSWORD
            server.login("chandusst987@gmail.com", "jiof corb rrbn gytq")

            server.send_message(msg)
            server.quit()

            st.success("✅ Email Sent Successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

# ================= MAP =================
with tab2:
    

    st.subheader(" Map")

    # ================= LOAD =================
    data = pd.read_csv("vij_hyd_labelled_dataset.csv")
    data.columns = data.columns.str.strip().str.lower()

    data = data.dropna(subset=["lat", "lon"]).copy()

    # ================= PREDICTION =================
    pred = model.predict(data[FEATURE_COLS])
    proba = model.predict_proba(data[FEATURE_COLS])

    data["predicted_source"] = le.inverse_transform(pred)
    data["confidence"] = proba.max(axis=1) * 100

    # ================= SEVERITY =================
    weights = {'pm2_5':0.4,'pm10':0.25,'no2':0.15,'o3':0.1,'so2':0.05,'co':0.05}

    data["severity"] = data.apply(
        lambda r: sum(r[p]*weights[p] for p in weights),
        axis=1
    )

    max_sev = data["severity"].max()
    data["severity_norm"] = data["severity"] / max_sev if max_sev != 0 else 0

    # ================= MAP =================
    m = folium.Map(
        location=[data["lat"].mean(), data["lon"].mean()],
        zoom_start=11,
        tiles="CartoDB positron"
    )

    # ================= HEATMAP =================
    HeatMap(
        data[["lat","lon","severity_norm"]].values.tolist(),
        radius=25,
        blur=30
    ).add_to(m)

    # ================= SOURCE COLORS =================
    source_colors = {
        "Industrial": "red",
        "Vehicular": "blue",
        "Agricultural": "green",
        "Burning": "orange",
        "Natural": "purple"
    }

    # ================= MARKERS =================
    for _, row in data.iterrows():

        popup = f"""
        <b>Location:</b> {row.get('location','N/A')}<br>
        <b>Source:</b> {row['predicted_source']}<br>
        <b>Confidence:</b> {row['confidence']:.2f}%<br>
        <b>Severity:</b> {row['severity']:.2f}
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            color=source_colors.get(row["predicted_source"], "gray"),
            fill=True,
            fill_opacity=0.7,
            popup=popup
        ).add_to(m)

    # ================= LEGEND =================
    legend_html = '''
    <div style="
    position: fixed;
    bottom: 30px; left: 50px; width: 250px;
    background-color: white; z-index:9999;
    border:2px solid grey; padding: 10px;">
    <b>Pollution Source</b><br>
    <span style="color:red;">● Industrial<br>
    <span style="color:blue;">●Vehicular<br>
    <span style="color:green;">● Agricultural<br>
    <span style="color:orange;">● Burning<br>
    <span style="color:purple;">● Natural<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # ================= DISPLAY =================
    st_folium(m, width=1000, height=900)

# ================= REPORT =================
with tab3:
    

    st.subheader(" Reports & Analysis")

    all_sources = ["Industrial","Vehicular","Agricultural","Burning","Natural"]

    source_counts = filtered_df["pollution_source"] \
        .value_counts() \
        .reindex(all_sources, fill_value=0)

    # TABLE
    st.write("### 📋 Source Table")
    table_df = source_counts.reset_index()
    table_df.columns = ["Source", "Count"]
    st.dataframe(table_df)

    # PIE
    # PIE (FIXED CLEAN VERSION)
    st.write("###  Pie Chart")

# ❌ Remove zero values
    clean_counts = source_counts[source_counts > 0]

    labels = clean_counts.index
    sizes = clean_counts.values

    colors = ["purple", "blue", "green", "red", "orange"]

# ✅ Hide small % text
    def autopct_format(pct):
    # Always show Vehicular OR show if > 2%
        if pct > 2:
          return f'{pct:.1f}%'
          

    fig, ax = plt.subplots(figsize=(5,5))

    wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    colors=colors[:len(labels)],
    autopct="%1.1f%%",   # ✅ show all %
    startangle=140,
    pctdistance=0.75,
    labeldistance=1.1
)

# Reduce font to avoid overlap
    for text in texts:
      text.set_fontsize(9)

    for autotext in autotexts:
      autotext.set_fontsize(8)

    ax.set_title("Pollution Source Distribution")
    plt.tight_layout()
    st.pyplot(fig)

    # LINE
    st.write("###  Trend")
    trend = filtered_df.groupby("hour")[pollutant].mean()
    st.line_chart(trend)

    # ================= TOP LOCATIONS =================
    st.subheader("Top Polluted Locations (PM2.5)")

    top_locations = (
       df.groupby("location")["pm2_5"]
       .mean()
       .sort_values(ascending=False)
       .head(5)
)

    st.bar_chart(top_locations)

# Optional table view
    top_df = top_locations.reset_index()
    top_df.columns = ["Location", "Avg PM2.5"]
    st.dataframe(top_df)

# ================= CHATBOT =================
import streamlit as st
import pandas as pd
from groq import Groq
import httpx
import re

with tab4:
    # --- 1. CSS: HIGH VISIBILITY FOR BUTTONS & TEXT ---
    st.markdown("""
        <style>
        /* Force the Browse Files button to be Solid Blue */
        [data-testid="stFileUploadDropzone"] button {
            background-color: #2563eb !important; 
            color: white !important;
            border: 2px solid white !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
            visibility: visible !important;
            display: block !important;
            font-weight: bold !important;
        }
        /* Make the drag-drop text dark and readable */
        [data-testid="stFileUploadDropzone"] label, [data-testid="stFileUploadDropzone"] p {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        /* Professional Help Box Styling */
        .help-container {
            background-color: #f0f9ff;
            border-left: 6px solid #0ea5e9;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            color: #1e293b;
            font-size: 0.95rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("💬 Environmental Data Analyst")

    # --- 2. DATA LOADING ---
    @st.cache_data
    def get_full_dataset():
        try:
            df = pd.read_csv("vij_hyd_labelled_dataset.csv")
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            st.error(f"Dataset not found: {e}")
            return None

    base_df = get_full_dataset()
    uploaded_files = st.file_uploader("Upload additional documents (PDF/CSV)", type=["csv", "pdf", "docx"], accept_multiple_files=True)

    # --- 3. CHAT INITIALIZATION ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I have access to all columns in the dataset (Pollution, Weather, Sources). Type **help** to see how to ask!"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # --- 4. COMMAND & ANALYSIS LOGIC ---
    if prompt := st.chat_input("Ask about a date, location, or weather..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- A. HELP COMMAND ---
        if prompt.lower().strip() == "help":
            help_msg = """
            <div class="help-container">
            <h3>📖 Assistant Guide</h3>
            <b>✅ You can ask questions like:</b>
            <ul>
                <li>"What was the pollution source at Zoo Park on 2026-02-05?"</li>
                <li>"Give me <b>weather details</b> for Hyderabad on 2026-03-10."</li>
                <li>"Compare PM2.5 levels between Somajiguda and Kanuru."</li>
                <li>"What hour is industrial pollution highest?"</li>
            </ul>
            <b>⚠️ Limitations & Rules:</b>
            <ul>
                <li><b>Date Range:</b> Feb 1, 2026 to March 31, 2026 only.</li>
                <li><b>Weather Details:</b> I only show Temp/Humidity/Wind if you specifically include the word 'weather' in your question.</li>
                <li><b>Data Scope:</b> I can read all 33 columns including distances to roads/industries.</li>
            </ul>
            </div>
            """
            with st.chat_message("assistant"): st.markdown(help_msg, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": "Displayed help guide."})

        # --- B. AI ANALYSIS ENGINE ---
        else:
            # 1. Detect Date and Location in prompt
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', prompt)
            
            # 2. Check if user specifically asked for weather details
            weather_terms = ["weather", "temp", "humidity", "wind", "pressure"]
            wants_weather = any(term in prompt.lower() for term in weather_terms)
            
            context_data = ""
            if date_match and base_df is not None:
                d = date_match.group(0)
                # Filter by date
                day_data = base_df[base_df['timestamp'].dt.date == pd.to_datetime(d).date()]
                
                # Further filter if a specific location is mentioned
                locations = base_df['location'].unique()
                for loc in locations:
                    # Clean the location name for matching
                    loc_short = loc.split(",")[0].lower()
                    if loc_short in prompt.lower():
                        day_data = day_data[day_data['location'].str.contains(loc_short, case=False)]
                
                if not day_data.empty:
                    # Pulling ALL important columns to ensure LLM has the full picture
                    context_data = day_data.head(20).to_string(index=False)

            # 3. Call AI with specific instructions
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # Instruction to control weather output
                weather_rule = "The user wants weather details. Report Temp, Humidity, Wind, and Pressure." if wants_weather else "Do NOT report weather details unless they explain a pollution spike."
                
                system_instr = (
                    f"You are a professional Environmental Data Analyst. {weather_rule}\n"
                    "Always mention the 'pollution_source' for the requested date and location.\n"
                    "If the user asks for a location/date not in the context, check the data carefully before saying it is missing.\n"
                    f"FULL DATA CONTEXT:\n{context_data if context_data else 'No specific data found for this query.'}"
                )

                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_instr}] + st.session_state.messages[-5:],
                    model="llama-3.3-70b-versatile",
                    temperature=0.1
                ).choices[0].message.content
                
                with st.chat_message("assistant"): st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

with tab5:
    import streamlit as st
    import requests
    import pandas as pd

    st.markdown(" Live Pollution Monitoring")

    # ================= API KEY =================
    API_KEY = "c630fe86123ccf82de5644158b421b80"  # 🔴 replace this

    if not API_KEY or API_KEY == "YOUR_OPENWEATHER_API_KEY":
        st.warning("⚠️ Please add your OpenWeather API key to enable live data")
        st.stop()

    # ================= CITY DATA =================
    city_coords = {
        "Hyderabad":     {"lat": 17.3850, "lon": 78.4867},
        "Vijayawada":    {"lat": 16.5062, "lon": 80.6480},
        "Chennai":       {"lat": 13.0827, "lon": 80.2707},
        "Delhi":         {"lat": 28.6139, "lon": 77.2090},
        "Mumbai":        {"lat": 19.0760, "lon": 72.8777},
        "Bengaluru":     {"lat": 12.9716, "lon": 77.5946},
        "Visakhapatnam": {"lat": 17.6801, "lon": 83.2016}
    }

    city_list = list(city_coords.keys())

    # ================= SESSION =================
    if "live_city" not in st.session_state:
        st.session_state.live_city = "Hyderabad"

    if "live_city_widget" not in st.session_state:
        st.session_state.live_city_widget = st.session_state.live_city

    def update_city():
        st.session_state.live_city = st.session_state.live_city_widget

    # ================= API CALL =================
    @st.cache_data(ttl=300)
    def get_live_pollution(city, key):
        coords = city_coords[city]

        url = "http://api.openweathermap.org/data/2.5/air_pollution"
        params = {"lat": coords["lat"], "lon": coords["lon"], "appid": key}

        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()

        item = data["list"][0]

        return {
            "AQI": item["main"]["aqi"],
            "PM2.5": item["components"].get("pm2_5"),
            "PM10": item["components"].get("pm10"),
            "NO2": item["components"].get("no2"),
            "O3": item["components"].get("o3"),
            "SO2": item["components"].get("so2"),
            "CO": item["components"].get("co"),
            "time": pd.Timestamp.now()
        }

    # ================= FORECAST =================
    @st.cache_data(ttl=300)
    def get_forecast(city, key):
        coords = city_coords[city]

        url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
        params = {"lat": coords["lat"], "lon": coords["lon"], "appid": key}

        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()

        rows = []
        for i in data["list"]:
            rows.append({
                "Time": pd.to_datetime(i["dt"], unit="s"),
                "AQI": i["main"]["aqi"],
                "PM2.5": i["components"].get("pm2_5"),
                "PM10": i["components"].get("pm10"),
                "So2": i["components"].get("so2"),
                "CO": i["components"].get("co"),
                "O3": i["components"].get("o3"),
                "NO2": i["components"].get("no2")
            })

        return pd.DataFrame(rows)

    # ================= AQI STATUS =================
    def get_aqi_status(aqi):
        return {
            1: "Good 🟢",
            2: "Fair 🟡",
            3: "Moderate 🟠",
            4: "Poor 🔴",
            5: "Very Poor 🛑"
        }.get(aqi, "Unknown")

    # ================= HEALTH =================
    def health_advice(aqi):
        if aqi == 1:
            return "Air quality is good. Enjoy outdoor activities."
        elif aqi == 2:
            return "Acceptable air quality. Sensitive individuals should be cautious."
        elif aqi == 3:
            return "Limit outdoor exposure. Consider wearing a mask."
        elif aqi == 4:
            return "Avoid outdoor activities. Wear N95 mask."
        else:
            return "Hazardous air quality. Stay indoors."

    # ================= UI =================
    col1, col2 = st.columns([1,5])

    with col1:
        if st.button(" Refresh"):
            st.cache_data.clear()
            st.rerun()

    st.selectbox(
        "Select City",
        city_list,
        key="live_city_widget",
        on_change=update_city
    )

    city = st.session_state.live_city
    st.write(f" Current City: **{city}**")

    # ================= DISPLAY =================
    try:
        data = get_live_pollution(city, API_KEY)

        def safe(x):
            return f"{x:.2f}" if x is not None else "N/A"

        # METRICS
        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)

        c1.metric("PM2.5", safe(data["PM2.5"]))
        c2.metric("PM10", safe(data["PM10"]))
        c3.metric("NO2", safe(data["NO2"]))
        c4.metric("O3", safe(data["O3"]))
        c5.metric("SO2", safe(data["SO2"]))
        c6.metric("CO", safe(data["CO"]))

        # AQI
        st.subheader(" Air Quality Index")
        st.metric("AQI", data["AQI"])
        st.success(get_aqi_status(data["AQI"]))

        # HEALTH
        st.subheader(" Health Advice")
        st.info(health_advice(data["AQI"]))

        st.caption(f"Updated: {data['time']}")

        # FORECAST
        st.subheader(" 4-Day Forecast")
        forecast = get_forecast(city, API_KEY)

        if not forecast.empty:
            st.dataframe(forecast, use_container_width=True)
            st.line_chart(forecast.set_index("Time"))
        else:
            st.warning("No forecast data available")

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")