from flask import Flask, render_template,Blueprint
from db import connect_payments

admin_p = Blueprint('ad_p', __name__, template_folder='../templates')

@admin_p.route('/payment_details', methods=['GET'])
def payment_details():
    # Connect to DB
    conn = connect_payments()
    # use dictionary cursor so rows can be accessed by column name in the template
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all payment records
    cursor.execute("SELECT * FROM payments ORDER BY stud_id asc")
    payments = cursor.fetchall()
    
    conn.close()
    
    # Render HTML template with payments
    return render_template('admin_paid.html', payments=payments)

