from flask import Flask, render_template, request, send_file,Blueprint,session,redirect,url_for
from db import connect_payments
from io import BytesIO
from reportlab.pdfgen import canvas

student_p = Blueprint('stud_pay', __name__, template_folder='../templates')


# -------------------
# Routes
# -------------------

@student_p.route('/pay', methods=['GET', 'POST'])
def pay():
    conn = connect_payments()
    cursor = conn.cursor(dictionary=True)

    # Fetch fixed amount for this student
    cursor.execute("SELECT amount FROM fees WHERE stud_id = %s", (session['id'],))
    fee_record = cursor.fetchone()

    if not fee_record:
        conn.close()
        return "No fee record found for this student.", 400

    fixed_amount = fee_record['amount']

    # Check if already paid
    cursor.execute("SELECT * FROM payments WHERE stud_id = %s ", (session['id'],))
    already_paid = cursor.fetchone()
    if already_paid:
        conn.close()
        return render_template('pay.html',already_paid=already_paid['amount'])

    if request.method == 'POST':
        amount = fixed_amount  # Force the system to use fixed amount only

        # Dummy payment ID
        payment_id = f"DUMMY-{session['username'][:3].upper()}-{amount*100:.0f}"

        # Store payment in MySQL
        cursor.execute(
            'INSERT INTO payments (name, stud_id, amount, payment_id, status) VALUES (%s,%s,%s,%s,%s)',
            (session['username'], session['id'], amount, payment_id, 'Success')
        )
        conn.commit()
        conn.close()

        # Generate PDF receipt in memory
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(150, 800, "Payment Receipt")
        p.setFont("Helvetica", 12)
        p.drawString(50, 750, f"Payment ID: {payment_id}")
        p.drawString(50, 730, f"Name: {session['username']}")
        p.drawString(50, 710, f"Student ID: {session['id']}")
        p.drawString(50, 690, f"Amount Paid: ₹{amount}")
        p.drawString(50, 670, "Status: Success")
        p.showPage()
        p.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"receipt_{payment_id}.pdf",
            mimetype='application/pdf'
        )

    # Show fixed amount to student before paying
    conn.close()

    return render_template("pay.html", fixed_amount=fixed_amount)