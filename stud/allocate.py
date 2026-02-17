import uuid
from flask import Flask, render_template, request, redirect, url_for, session,Blueprint,send_file
from db import connect_hostel

from io import BytesIO
from reportlab.pdfgen import canvas

student_al = Blueprint('stud_alloc', __name__, template_folder='../templates')





# -------------------
# Student Login (simple by username)
# -------------------
@student_al.route("/hos")
def hos():
    username=session.get("username")
    conn = connect_hostel()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE username=%s", (username,))
    student = cur.fetchone()
    conn.close()
    if student:
        session["student_id"] = student["id"]
        session["username"] = student["username"]
        return redirect(url_for("stud_alloc.dashboard"))
    else:
        return "Invalid Username"

# -------------------
# Dashboard
# -------------------
@student_al.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("stud_alloc.hos"))
    student_id = session["student_id"]
    conn = connect_hostel()
    cur = conn.cursor(dictionary=True)

    # check allocation
    cur.execute("""
        SELECT s.name, s.email, h.name as hostel_name, r.room_no, a.allocated_at
        FROM allocations a
        JOIN students s ON a.student_id = s.id
        JOIN rooms r ON a.room_id = r.id
        JOIN hostels h ON r.hostel_id = h.id
        WHERE s.id=%s
    """, (student_id,))
    allocation = cur.fetchone()

    # check payment
    cur.execute("SELECT * FROM payments WHERE student_id=%s AND status='Success'", (student_id,))
    payment = cur.fetchone()

    conn.close()
    return render_template("hostel.html", allocation=allocation, payment=payment)

# -------------------
# Make Payment (dummy)
# -------------------
@student_al.route("/pays", methods=["GET", "POST"])
def pays():
    conn = connect_hostel()
    cursor = conn.cursor(dictionary=True)

    # Fetch fixed amount for this student
    cursor.execute("SELECT amount FROM fees WHERE stud_id = %s", (session['id'],))
    fee_record = cursor.fetchone()

    if not fee_record:
        conn.close()
        return "No fee record found for this student.", 400

    fixed_amount = fee_record['amount']

    # Check if already paid
    cursor.execute("SELECT * FROM payments WHERE student_id = %s", (session['id'],))
    already_paid = cursor.fetchone()
    if already_paid:
        conn.close()
        return render_template('hostel.html',payment=already_paid,)

    if request.method == 'POST':
        amount = fixed_amount  # Force the system to use fixed amount only

        # Dummy payment ID
        payment_id = f"DUMMY-{session['username'][:3].upper()}-{amount*100:.0f}"

        # Store payment in MySQL
        cursor.execute(
            'INSERT INTO payments (status, student_id, amount, txn_id) VALUES (%s,%s,%s,%s)',
            ('Success', session['id'], amount, payment_id)
        )
        conn.commit()
        conn.close()

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

    return render_template("payment.html",fixed_amount=fixed_amount,)

# -------------------
# Allocate Room (only if paid)
# -------------------
@student_al.route("/allocate", methods=["GET", "POST"])
def allocate():
    if "student_id" not in session:
        return redirect(url_for("stud_alloc.hos"))

    student_id = session["student_id"]
    conn = connect_hostel()
    cur = conn.cursor(dictionary=True)

    # check payment
    cur.execute("SELECT * FROM payments WHERE student_id=%s AND status='Success'", (student_id,))
    payment = cur.fetchone()
    if not payment:
        conn.close()
        return "You must pay before allocation! <a href='{}'>Pay Here</a>".format(url_for("stud_alloc.pays"))

    # check if already allocated
    cur.execute("SELECT * FROM allocations WHERE student_id=%s", (student_id,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return redirect(url_for("stud_alloc.dashboard"))

    if request.method == "POST":
        room_id = request.form.get("room_id")

        if not room_id:
            conn.close()
            return "Please select a room!"

        # confirm room exists and available
        cur.execute("SELECT * FROM rooms WHERE room_no=%s AND available > 0", (room_id,))
        room = cur.fetchone()

        if not room:
            conn.close()
            return "Selected room is no longer available!"

        # allocate
        cur.execute("INSERT INTO allocations (student_id, room_id) VALUES (%s,%s)", (student_id, room["id"]))
        cur.execute("UPDATE rooms SET available = available - 1 WHERE id=%s", (room["id"],))
        conn.commit()
        conn.close()

        return redirect(url_for("stud_alloc.dashboard"))

    # GET request → fetch available rooms
    cur.execute("SELECT id, room_no, floor, capacity, available FROM rooms WHERE available > 0")
    available_rooms = cur.fetchall()

    conn.close()

    # DEBUG: print in console to see what is fetched
    print("Available rooms:", available_rooms)

    return render_template("hostel2.html", available_rooms=available_rooms)