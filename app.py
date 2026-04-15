# ===============================
#  IMPORT LIBRARIES
# ===============================
import streamlit as st
import pandas as pd
import os, json, re, requests
from datetime import datetime
import xml.etree.ElementTree as ET

# ===============================
#  PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Ad Tags TXT File Generator",
    page_icon="🧾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===============================
#  GLOBAL CSS 
# ===============================
css = """
<style>

/* Main app */
.stApp {
    background-color: #f6f7fb;
    color: #1f2937;
    font-family: "Inter", system-ui, sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 0.45rem 1rem;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Download button */
.stDownloadButton > button {
    background-color: #16a34a;
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background-color: #15803d;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

div[data-testid="metric-container"] label {
    color: #6b7280;
    font-weight: 600;
}

div[data-testid="metric-container"] div {
    font-size: 1.4rem;
    font-weight: 700;
    color: #111827;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
    padding: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

/* Inputs */
input, textarea, select {
    border-radius: 8px !important;
}

/* Remove fullscreen button */
button[title="View fullscreen"] {
    display: none !important;
}

</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ===============================
#  USER PREFERENCE STORAGE
# ===============================
PREF_FILE = "user_prefs.json"

def load_prefs(email):
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE) as f:
            data = json.load(f)
            return data.get(email, {})
    return {}

def save_prefs(email, prefs):
    data = {}
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE) as f:
            data = json.load(f)
    data[email] = prefs
    with open(PREF_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ===============================
#  AUTHENTICATION
# ===============================
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return

    st.image("excel_to_dcm_vast_txt_generator_tool.png", width=220)
    st.markdown("## 🔐 Secure Login")
    st.caption("Authorized users only")

    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.secrets.get("auth", {}).get("users", {})
        password = st.secrets.get("auth", {}).get("password")
        if email in users and pwd == password:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            prefs = load_prefs(email)
            st.session_state.dark_pref = prefs.get("dark", False)
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

authenticate()

# ===============================
#  SIDEBAR
# ===============================
with st.sidebar:
    st.image("excel_to_dcm_vast_txt_generator_tool.png", width=160)
    st.markdown("### 🎯 Jatin Bhardwaj Project")
    st.caption("Industry: Ad Tech  \nRole: Data Analyst  \nProject: Tags TXT Generator Tool")
    st.markdown("---")

    st.markdown("**🌗 Appearance**")
    dark_pref = st.checkbox("Prefer Dark Mode", value=st.session_state.get("dark_pref", False))
    if dark_pref != st.session_state.get("dark_pref"):
        st.session_state.dark_pref = dark_pref
        save_prefs(st.session_state.user_email, {"dark": dark_pref})
    st.caption("🌙 Theme applies on next reload")
    st.markdown("---")

    st.markdown("**🚀 Workflow**")
    st.markdown(
        "• Upload file  \n• Select sheet  \n• Include / Exclude rows  \n"
        "• Select columns  \n• Select Channel & Region  \n• Generate TXT  \n• Download TXT"
    )
    st.markdown("---")
    st.caption(f"👤 {st.session_state.user_email}")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ===============================
#  HEADER
# ===============================
st.markdown("## 🧾 Ad Tags TXT File Generator")
st.caption("Convert Excel / CSV files into formatted TXT — fast & secure")
st.markdown("---")

# ===============================
#  HELPERS
# ===============================
def clean_columns(df):
    df.columns = [str(c).strip() for c in df.columns]
    return df

def parse_row_ranges(text, max_rows):
    indexes = set()
    if not text.strip():
        return indexes
    for part in text.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            for i in range(int(start), int(end) + 1):
                if 1 <= i <= max_rows:
                    indexes.add(i - 1)
        else:
            i = int(part)
            if 1 <= i <= max_rows:
                indexes.add(i - 1)
    return indexes

# ===============================
#  HEADER AUTO-DETECTION 
# ===============================
def read_excel_with_real_header(file, sheet_name):
    raw = pd.read_excel(file, sheet_name=sheet_name, header=None)
    header_row = None

    for i, row in raw.iterrows():
        if "Placement ID" in row.astype(str).values:
            header_row = i
            break

    if header_row is None:
        st.error("❌ Header row with 'Placement ID' not found")
        st.stop()

    df = pd.read_excel(file, sheet_name=sheet_name, header=header_row)
    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
    df.columns = df.columns.astype(str).str.strip()
    return df

# ===============================
#  DCM MACROS 
# ===============================
def inject_macros(js_tag, channel, region):
    lines = js_tag.split("\n")
    if any("data-dcm-click-tracker" in l for l in lines):
        return js_tag

    click = device = app = None

    if channel == "IDSP":
        click = "data-dcm-click-tracker='$HTML_ESC_CLICK_URL'"
        device = "$DEVICE_ID"
        if region == "NA":
            app = "$SITE_APP_ID"
    else:
        click = "data-dcm-click-tracker='{{CLICK_URL_ESC}}'"
        device = "{{USER_ID}}"
        if region == "NA":
            app = "{{SITE_ID}}"

    lines.insert(3, f"    {click}")
    lines.insert(4, "    data-dcm-landing-page-escapes=0")

    for i, line in enumerate(lines):
        if "data-dcm-resettable-device-id" in line:
            lines[i] = f"    data-dcm-resettable-device-id='{device}'"
        if app and "data-dcm-app-id" in line:
            lines[i] = f"    data-dcm-app-id='{app}'>"

    return "\n".join(lines)

# ===============================
#  VAST MACROS 
# ===============================
def is_vpaid_from_tag_or_xml(vast_url):
    try:
        r = requests.get(vast_url, timeout=6)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        for el in root.iter():
            if el.tag.endswith("MediaFile") and el.attrib.get("apiFramework","").strip().upper()=="VPAID":
                return True
    except:
        pass
    return False

def apply_vast_macros(url, channel):
    url = re.sub(
        r"ord=[^;&]*",
        "ord=$CACHEBUSTER" if channel=="IDSP" else "ord={{CACHEBUSTER}}",
        url
    )

    url = re.sub(
        r"dc_sdk_apis=(\[APIFRAMEWORKS\]|%5BAPIFRAMEWORKS%5D)",
        "dc_sdk_apis=7",
        url,
        flags=re.IGNORECASE
    )

    return url

# ===============================
#  DOWNLOAD TOAST HELPER
# ===============================
def show_download_toast():
    st.toast("Download started", icon="⬇️")

# ===============================
#  TAG TYPE
# ===============================
tag_type = st.radio("Choose Tag Type", ["DCM","VAST"])

# ===============================
#  FILE UPLOAD
# ===============================
if "file_version" not in st.session_state:
    st.session_state.file_version = 0

uploaded_file = st.file_uploader(
    "Upload file",
    type=["xls","xlsx","csv"],
    key=f"file_uploader_{st.session_state.file_version}"
)

if uploaded_file is None:
    st.stop()

st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

if st.button("Reload / Re-upload File"):
    st.session_state.file_version += 1
    st.rerun()

# ===============================
#  RESET STATE ON FILE CHANGE
# ===============================
if "last_file_version" not in st.session_state or st.session_state.last_file_version != st.session_state.file_version:
    st.session_state.last_file_version = st.session_state.file_version
    for k in list(st.session_state.keys()):
        if k not in ["authenticated","user_email","file_version","last_file_version"]:
            st.session_state.pop(k,None)

# ===============================
#  DYNAMIC WORKFLOW HEADING
# ===============================
if uploaded_file:
    if tag_type == "DCM":
        st.markdown("## 🧾 DCM Tags Generator")
    elif tag_type == "VAST":
        st.markdown("## 🧾 VAST Tags Generator")

# ===============================
#  DCM WORKFLOW
# ===============================
if tag_type=="DCM":
    xls = pd.ExcelFile(uploaded_file)
    sheet = st.selectbox("Select sheet", xls.sheet_names)
    df = read_excel_with_real_header(uploaded_file,sheet)
    df = clean_columns(df)

    original_df = df.copy()
    total_rows = len(df)
    included_indexes = set()
    excluded_indexes = set()

    include_text = st.text_input("Include rows (optional)")
    exclude_text = st.text_input("Exclude rows (optional)")

    if include_text:
        included_indexes = parse_row_ranges(include_text, total_rows)
        df = df.iloc[sorted(included_indexes)]
    if exclude_text:
        excluded_indexes = parse_row_ranges(exclude_text, total_rows)
        df = df.drop(df.index[list(excluded_indexes)], errors="ignore")

    cols = st.multiselect("Select Columns", df.columns.tolist())
    if cols:
        df = df[cols]

    included_count = len(included_indexes) if include_text else total_rows
    excluded_count = len(excluded_indexes)
    final_count = len(df)

    st.markdown("### 📊 Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total rows", total_rows)
    c2.metric("Included rows", included_count)
    c3.metric("Excluded rows", excluded_count)
    c4.metric("Final rows", final_count)

    channel = st.selectbox("Channel", ["IDSP","BEESWAX"])
    region = st.selectbox("Region", ["NA","NON-NA"])

    st.dataframe(df.head(10))

    if st.button("Generate TXT"):
        output = []
        for _, row in df.iterrows():
            for col in df.columns:
                val = str(row[col])
                if "<ins class='dcmads'" in val:
                    val = inject_macros(val,channel,region)
                output.append(f"{col} - {val}")
                if col.strip().lower() == "placement id":
                    output.append("-"*100)
            output.append("-"*100)

        txt = "\n".join(output)
        st.success("✅ Generated TXT Tags File Successfully")

        st.download_button(
            "Download TXT",
            txt,
            file_name=f"DCM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            on_click=show_download_toast
        )

# ===============================
#  VAST WORKFLOW
# ===============================
if tag_type=="VAST":
    xls = pd.ExcelFile(uploaded_file)
    sheet = st.selectbox("Select sheet", xls.sheet_names)
    df = read_excel_with_real_header(uploaded_file,sheet)
    df = clean_columns(df)

    original_df = df.copy()
    total_rows = len(df)
    included_indexes = set()
    excluded_indexes = set()

    include_text = st.text_input("Include rows (optional)")
    exclude_text = st.text_input("Exclude rows (optional)")

    if include_text:
        included_indexes = parse_row_ranges(include_text, total_rows)
        df = df.iloc[sorted(included_indexes)]
    if exclude_text:
        excluded_indexes = parse_row_ranges(exclude_text, total_rows)
        df = df.drop(df.index[list(excluded_indexes)], errors="ignore")

    cols = st.multiselect("Select Columns", df.columns.tolist())
    if cols:
        df = df[cols]

    included_count = len(included_indexes) if include_text else total_rows
    excluded_count = len(excluded_indexes)
    final_count = len(df)

    st.markdown("### 📊 Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total rows", total_rows)
    c2.metric("Included rows", included_count)
    c3.metric("Excluded rows", excluded_count)
    c4.metric("Final rows", final_count)

    channel = st.selectbox("Channel", ["IDSP","BEESWAX"])
    st.dataframe(df.head(10))

    if st.button("Generate TXT"):

        vast_col = [c for c in df.columns if "VAST" in c.upper()][0]
        output = []

        for _, row in df.iterrows():

            placement_name = row.get("Placement Name", "")
            placement_id = row.get("Placement ID", "")

            url = apply_vast_macros(str(row[vast_col]), channel)

            output.append(f"Placement Name - {placement_name}")
            output.append(f"Placement ID - {placement_id}")
            output.append("-"*100)
            output.append(f"VAST Tag - {url}")
            output.append("-"*100)

        txt = "\n".join(output)

        st.success("✅ Generated TXT Tags File Successfully")

        st.download_button(
            "Download TXT",
            txt,
            file_name=f"VAST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            on_click=show_download_toast
        )
