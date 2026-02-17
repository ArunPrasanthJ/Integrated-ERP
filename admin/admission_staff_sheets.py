from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint
import pandas as pd
from db import connect_details
import requests
import re
from io import StringIO

admin_s = Blueprint('ad_s', __name__, template_folder='../templates')


# Helper to get details DB connection
def get_db_connection():
    return connect_details()

# Show all sheet links
@admin_s.route("/sheet_index")
def sheet_index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM google_forms ORDER BY id DESC")
    sheets = cursor.fetchall()
    conn.close()
    return render_template("ad_sheets.html", sheets=sheets)

# Add new sheet link
@admin_s.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    sheet_url = request.form["sheet_url"]
    sheet_id=request.form["sheet_id"]
    form_id=request.form["form_id"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO google_forms (form_name,form_id,sheet_id,sheet_url) VALUES (%s, %s,%s,%s)", (name, form_id,sheet_id,sheet_url))
    conn.commit()
    conn.close()
    flash("✅ Sheet link added successfully!")
    return redirect(url_for("ad_s.sheet_index"))

# Import all sheets into D

def sanitize_columns(df):
    """Sanitize DataFrame column names for safe MySQL usage."""
    new_cols, used = [], set()
    for idx, col in enumerate(df.columns):
        safe_col = re.sub(r'\W+', '_', str(col).strip())  # keep only alphanum + _
        if not safe_col:
            safe_col = f"col_{idx}"  # fallback if blank
        while safe_col in used:
            safe_col += "_1"
        used.add(safe_col)
        new_cols.append(safe_col)
    df.columns = new_cols
    return df

@admin_s.route("/import_selected", methods=["GET", "POST"])
def import_selected():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch form options for dropdown
    cursor.execute("SELECT form_name, sheet_id FROM google_forms")
    forms = cursor.fetchall()

    if request.method == "POST":
        form_name = request.form.get("form_name")

        # Get the sheet_id for the chosen form
        cursor.execute("SELECT sheet_id FROM google_forms WHERE form_name = %s", (form_name,))
        sheet = cursor.fetchone()

        if not sheet:
            flash("❌ Invalid form selected!")
            return redirect(url_for("admin_s.import_selected"))

        url = sheet["sheet_id"]

        try:
            csv_data = requests.get(url).text
        except Exception as e:
            flash(f"❌ Error fetching {url}: {e}")
            return redirect(url_for("admin_s.import_selected"))

        # Read CSV
        df = pd.read_csv(StringIO(csv_data), on_bad_lines="skip", engine="python")

        # Sanitize column names
        df = sanitize_columns(df)

        # Drop old table
        cursor.execute(f"DROP TABLE IF EXISTS `{form_name}`")

        # Build CREATE TABLE query (all TEXT for simplicity)
        col_defs = [f"`{col}` TEXT" for col in df.columns]
        create_query = f"""
        CREATE TABLE `{form_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {', '.join(col_defs)}
        )
        """
        cursor.execute(create_query)

        # Insert rows
        cols = ", ".join([f"`{c}`" for c in df.columns])
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO `{form_name}` ({cols}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            values = [str(v) if pd.notna(v) else None for v in row]
            cursor.execute(insert_query, values)

        conn.commit()
        flash(f"✅ Form {form_name} imported successfully!")
        return redirect(url_for("ad_s.import_selected"))

    conn.close()
    return render_template("ad_sheets.html", forms=forms)






