from flask import Flask, render_template, request,Blueprint
from db import connect_details

admin_t=Blueprint('ad_t', __name__, template_folder='../templates')
# (no local DB helper) 

@admin_t.route("/table", methods=["GET", "POST"])
def table():
    data = []
    columns = []
    table_name = ""

    if request.method == "POST":
        table_name = request.form["table_name"]

        try:
            conn = connect_details()
            cursor = conn.cursor()

            # ⚠️ Protect from SQL injection by allowing only valid table names
            cursor.execute("SHOW TABLES")
            valid_tables = [row[f"Tables_in_{conn.db.decode()}"] for row in cursor.fetchall()]

            if table_name in valid_tables:
                cursor.execute(f"SELECT * FROM `{table_name}`")
                data = cursor.fetchall()
                if data:
                    columns = list(data[0].keys())
            else:
                data = []
                columns = []
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()

    return render_template("ad_table.html", data=data, columns=columns, table_name=table_name)


