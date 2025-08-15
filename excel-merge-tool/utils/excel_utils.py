import pandas as pd

# Define the final set of columns
FINAL_COLUMNS = [
    "אזור", "גוש", "הערות_לעצים", "חלקה", "מבקש", "מספר", "מספר_עצים", "מספר_רשיון",
    "מקום_הפעולה", "מתאריך", "סוג_העץ", "סיבה", "עד_תאריך", "פעולה", "פרטי_הסיבה",
    "רחוב", "שם_העץ", "שם_מאשר", "תאריך_אחרון_להגשת_ערער", "תאריך_הרשיון", "תפקיד_מאשר"
]

# Mapping of possible column names to the standard
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

def clean_and_standardize(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame: remove unnamed columns, rename to standard names, add missing columns."""
    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Rename columns based on mapping
    df = df.rename(columns=lambda col: COLUMN_MAPPING.get(col.strip(), col.strip()))

    # Add missing columns with NaN
    for col in FINAL_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Return DataFrame with columns in correct order
    return df[FINAL_COLUMNS]
