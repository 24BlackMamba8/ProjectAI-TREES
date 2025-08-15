import streamlit as st
import pandas as pd
import os
import tempfile
import base64
import importlib

# ---------------- הגדרות עמוד ---------------- #
st.set_page_config(page_title="🚀 כלי מיזוג קבצי אקסל", layout="centered")

# ---------------- עיצוב CSS ---------------- #
st.markdown("""
<style>
/* רקע שקוף-לבן על התוכן */
.block-container {
    background: rgba(255, 255, 255, 0.85);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.25);
    max-width: 650px;
    margin: auto;
    font-family: 'Segoe UI', sans-serif;
}

/* כותרת ראשית */
.custom-title {
    font-size: clamp(20px, 2.8vw, 30px);
    font-weight: bold;
    text-align: center;
    color: #2F4F4F;
    margin-bottom: 10px;
}

/* כותרת משנה */
.custom-subtitle {
    font-size: clamp(16px, 2vw, 22px);
    text-align: center;
    color: #4F4F4F;
    margin-bottom: 20px;
}

/* כפתורים */
div.stButton > button {
    background-color: #228B22;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #2E8B57;
    transform: scale(1.05);
}

/* טבלאות */
.stDataFrame, .dataframe {
    font-size: 14px !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- רקע מתמונה מקומית ---------------- #
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("static/background.jpeg")

# ---------------- מבנה עמוד ---------------- #
st.markdown('<div class="custom-title">🚀 כלי מיזוג קבצי אקסל - רחובות של עצים 📂</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">איחוד קבצי אקסל לקובץ אחיד בלחיצה אחת</div>', unsafe_allow_html=True)

# ---------------- עמודות נדרשות ---------------- #
FINAL_COLUMNS = [
    "אזור", "גוש", "הערות_לעצים", "חלקה", "מבקש", "מספר", "מספר_עצים", "מספר_רשיון",
    "מקום_הפעולה", "מתאריך", "סוג_העץ", "סיבה", "עד_תאריך", "פעולה", "פרטי_הסיבה",
    "רחוב", "שם_העץ", "שם_מאשר", "תאריך_אחרון_להגשת_ערער", "תאריך_הרשיון", "תפקיד_מאשר"
]

COLUMN_MAPPING = {
    "אזור": "אזור",
    "גוש": "גוש",
    "הערות לעץ": "הערות_לעצים",
    "חלקה": "חלקה",
    "מבקש": "מבקש",
    "מספר": "מספר",
    "מספר עצים": "מספר_עצים",
    "מספר רשיון": "מספר_רשיון",
    "מקום הפעולה": "מקום_הפעולה",
    "מתאריך": "מתאריך",
    "סוג העץ": "סוג_העץ",
    "סיבה": "סיבה",
    "עד תאריך": "עד_תאריך",
    "פעולה": "פעולה",
    "פרטי הסיבה": "פרטי_הסיבה",
    "רחוב": "רחוב",
    "שם העץ": "שם_העץ",
    "שם מאשר": "שם_מאשר",
    "תאריך אחרון להגשת ערער": "תאריך_אחרון_להגשת_ערער",
    "תאריך הרשיון": "תאריך_הרשיון",
    "תפקיד מאשר": "תפקיד_מאשר"
}

# ---------------- פונקציית ניקוי ---------------- #
def clean_and_standardize(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.astype(str)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.rename(columns=lambda col: COLUMN_MAPPING.get(col.strip(), col.strip()))
    for col in FINAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[FINAL_COLUMNS]

# ---------------- העלאת קבצים ---------------- #
uploaded_files = st.file_uploader(
    "📂 העלה את כל קבצי האקסל שברצונך למזג",
    type=["xlsx", "xls", "xlsm", "xlsb", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"הועלו {len(uploaded_files)} קבצים")

    if st.button("🚀 בצע מיזוג"):
        st.info("מתחיל תהליך מיזוג... אנא המתן")

        # בדיקת xlrd עבור קבצי xls
        try:
            importlib.import_module("xlrd")
        except ImportError:
            st.warning("⚠️ כדי לקרוא קבצי XLS יש להתקין את הספרייה: pip install xlrd>=2.0.1")

        dataframes = []
        for file in uploaded_files:
            try:
                if file.name.lower().endswith(".csv"):
                    df = pd.read_csv(file, encoding="utf-8", low_memory=False)
                else:
                    df = pd.read_excel(file)
                df = clean_and_standardize(df)
                df["source_file"] = file.name
                dataframes.append(df)
                st.write(f"✅ נטען: {file.name} ({len(df)} שורות)")
            except Exception as e:
                st.warning(f"⚠️ לא ניתן לקרוא את {file.name}: {e}")

        if dataframes:
            merged_df = pd.concat(dataframes, ignore_index=True)
            merged_df.drop_duplicates(inplace=True)
            merged_df.fillna("", inplace=True)
            merged_df = merged_df[FINAL_COLUMNS + ["source_file"]]

            temp_dir = tempfile.mkdtemp()
            excel_path = os.path.join(temp_dir, "merged.xlsx")
            csv_path = os.path.join(temp_dir, "merged.csv")
            merged_df.to_excel(excel_path, index=False)
            merged_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

            st.success("✅ המיזוג הושלם בהצלחה!")
            st.write(f"סה\"כ שורות: {len(merged_df)}")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 הורד כ-Excel", data=open(excel_path, "rb"), file_name="merged.xlsx")
            with col2:
                st.download_button("📥 הורד כ-CSV", data=open(csv_path, "rb"), file_name="merged.csv")

            st.write("🔍 תצוגה מקדימה של 10 שורות ראשונות:")
            st.dataframe(merged_df.head(10))
        else:
            st.error("❌ לא נטענו נתונים תקינים.")
