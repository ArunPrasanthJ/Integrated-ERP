# Project Overview

This repository contains a Flask application for a simple student/admin portal with attendance, marks, payments, hostel allocation, and Google Form import features.

## Database Schema

The application interacts with several MySQL databases. The following sections document the tables and data structures used across the project. Schemas are inferred from the Python code and SQL statements present in the project.

### `test1` Database

- **users**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `username` (VARCHAR)
  - `password` (VARCHAR)
  - `role` (VARCHAR) – values include `student`, `staff`, `admin`, etc.

> **Staff-specific tables/fields:** none beyond the shared `users` table;
> the staff portal is mostly front‑end driven and currently reads student data
> from the same tables used by students. You can extend the schema with
> `staff_attendance`, `staff_marks`, etc., if you want to record faculty
> performance separately.

- **query_messages**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `sender` (VARCHAR)
  - `student_username` (VARCHAR)
  - `message` (TEXT)
  - `created_at` (TIMESTAMP) – inserted automatically by MySQL with `CURRENT_TIMESTAMP` in code.

- **ca1**
  - Contains student marks; queried by `name` field, with other columns not explicitly defined in code.
  - Suggested fields: `id`, `name`, plus various mark/subject columns.

- **attendance**
  - `username` (VARCHAR)
  - `percent` (FLOAT/INT)

- **day_attendance**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `date` (DATE or DATETIME)
  - `status` (VARCHAR) – e.g. `Present`, `Absent`, `Leave`
  - `username` (VARCHAR)

> Other tables may exist (e.g. for staff or additional features) but are not referenced in the current code.

### `payments_db` Database

The `Data base` folder contains two SQL dumps for this schema.  The structures are reproduced below:

```sql
-- from payments_db_payments.sql
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `stud_id` int DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `payment_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
```

```sql
-- from payments_db_fees.sql
CREATE TABLE `fees` (
  `stud_id` int NOT NULL,
  `amount` int DEFAULT NULL,
  PRIMARY KEY (`stud_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

- **payments**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `name` (VARCHAR) – student name for the payment
  - `stud_id` or `student_id` (INT) – foreign key to `users.id` or `students.id`
  - `amount` (FLOAT)
  - `payment_id` or `txn_id` (VARCHAR) – unique transaction identifier
  - `status` (VARCHAR) – e.g. `Success` (only used in hostel allocation flow)

- **fees**
  - `stud_id` (INT)
  - `amount` (FLOAT)

> Note: The `payments` table is used by two different modules with slightly different column names; the actual table should accommodate both sets of columns.

### `details` Database

A sample dump from the project illustrates how dynamic tables may look.  For example, the file
`details_workshop feedback.sql` created a table called `workshop feedback`:

```sql
CREATE TABLE `workshop feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Timestamp` text,
  `Feedback_Type` text,
  `Feedback` text,
  `Suggestions_for_improvement` text,
  `Name` text,
  `Email` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
```

The persistent metadata table used by several modules is defined as:

```sql
CREATE TABLE `google_forms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `form_name` varchar(255),
  `form_id` varchar(255),
  `sheet_id` varchar(255),
  `sheet_url` varchar(255),
  PRIMARY KEY (`id`)
);
```

- **google_forms**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `form_name` (VARCHAR)
  - `form_id` (VARCHAR)
  - `sheet_id` (VARCHAR)
  - `sheet_url` (VARCHAR)

- **Dynamic tables**
  - When a Google Sheets link is imported, a new table named after `form_name` is created. All columns are defined as `TEXT` and correspond to sanitized column headers from the CSV export of the sheet. Each such table has:
    - `id` (INT, primary key, AUTO_INCREMENT)
    - one `TEXT` column for each sheet column (names are sanitized to be MySQL-safe).

### `hostel_mgmt` Database

- **students**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `username` (VARCHAR)
  - `email` (VARCHAR) – referenced in allocation summary
  - Additional fields may exist.

- **rooms**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `room_no` (VARCHAR)
  - `floor` (INT)
  - `capacity` (INT)
  - `available` (INT)

- **allocations**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `student_id` (INT)
  - `room_id` (INT)
  - `allocated_at` (DATETIME or TIMESTAMP)

- **payments**
  - `id` (INT, primary key, AUTO_INCREMENT)
  - `status` (VARCHAR)
  - `student_id` (INT)
  - `amount` (FLOAT)
  - `txn_id` (VARCHAR)

- **fees**
  - `stud_id` (INT)
  - `amount` (FLOAT)

---

💡 **Reminder:** The actual database schemas should be created using `CREATE TABLE` statements when setting up the MySQL server. The definitions above are a reference based on access patterns found in the code. Adjust column types, constraints, and indexes as needed for production.

### 📁 "Data base" Folder

The repository includes a `Data base` directory containing SQL dump files extracted from the live databases.  These files reflect the exact table definitions and some sample data currently in use:

- `payments_db_payments.sql` – structure and rows for the `payments` table in `payments_db`.
- `payments_db_fees.sql` – definition and data for the `fees` table in `payments_db`.
- `details_workshop feedback.sql` – example dynamic table created when importing a Google Sheet.

You can inspect or run these dumps manually with `mysql < file.sql` if you need to reproduce the original state.

### Staff Interface & Styling

Although most of the Python code is focused on the student and admin flows, the
repository includes a fully‑styled staff dashboard (`templates/Staff_Dashboard.html`) with
placeholder data.  Staff users are nothing more than `users` records with
`role = 'staff'`, so no additional tables are required to log them in.  The
front end exposes sections for attendance, results/marks and a timetable which
can easily be wired up to the same `attendance`, `ca1` and `fees/payments`
queries used elsewhere.

Key CSS classes used by the staff UI:

- `.data-table`, `.data-table th`, `.data-table td` – generic table styling for
  lists of students, attendance rows, etc.
- `.status-present`, `.status-absent` – coloured badges used in the attendance
  view.
- `.staff-selector`, `.staff-option`, `.staff-option.active` – horizontal
  selector allowing a user to switch between different faculty profiles.
- Responsive rules under `@media (max-width: …)` adjust the sidebar and card
  grid for smaller screens.

#### Python module & templates

A new `staff/` package supplies route handlers and lightweight views:

- `staff/staff_dashboard.py` &ndash; blueprint that registers `/staff/attendance`
  and `/staff/results` routes and renders the supporting templates.  It uses
  the same `test1` database connection helpers as the student modules.
- Templates in `templates/staff/` now extend a common admin‑style layout:
  `staff/staff_base.html` contains the full CSS and sidebar/topbar markup
  copied from `a_dash.html` so the staff pages share the exact visual theme.
  Individual pages (`staff_attendance.html`, `staff_results.html`) define only
  their table content in a `{% block content %}`.
- A stylesheet `static/css/staff.css` remains for any additional rules but is
  no longer strictly necessary since most styling lives in `staff_base.html`.


#### Staff routes
- `/staff/attendance` &ndash; list all student attendance rows with status badges.
- `/staff/attendance_entry` &ndash; form for staff to insert new attendance records and view the same table in one place (separate blueprint file).
- `/staff/results` &ndash; display the contents of the `ca1` marks table. (Read‑only)
- `/staff/marks_entry` &ndash; subject‑wise marks entry page; staff can add/update marks per student and see the complete table.

(These are registered by the `staff_bp` blueprint imported in `login.py`.)

The `login.py` entry point now imports and registers `staff_bp` so staff logins
automatically gain access to the new endpoints.

If you later decide to track staff attendance or internal marks, you can add
new tables such as `staff_attendance` or `staff_reviews` and mirror the SQL
initialiser in `db_setup.py`.

### 🔧 Automatic Schema Creation

### 🧱 Centralized Database Connection Helpers

To reduce duplication and make configuration changes easier, all modules now
obtain MySQL connections through a single helper file `db.py`.  Rather than
copying connection details into every blueprint, each Python file simply
imports one of the provided functions:

```python
from db import connect_test1, connect_payments, connect_details, connect_hostel

conn = connect_test1()          # users/attendance/marks
conn = connect_payments()       # general payments/fees
conn = connect_details()        # dynamic google form tables
conn = connect_hostel()         # hostel management schema
```

The `connect` function contained in `db.py` picks the appropriate driver
(`pymysql` or `mysql.connector`) and applies the shared credentials defined
in the `BASE_CONFIG` dictionary.  This refactor eliminated dozens of
`get_db_connection()` helpers scattered throughout the project and ensures
that a single change to a hostname, user, or password is applied everywhere.

### 🔧 Automatic Schema Creation

To make onboarding easier, a helper module `db_setup.py` is provided.  When the Flask application starts (or when you run `python db_setup.py` directly), it will:

1. Create the four databases (`test1`, `payments_db`, `details`, `hostel_mgmt`) if they do not exist.
2. Create every table used by the application using `CREATE TABLE IF NOT EXISTS` statements.
3. Leave dynamic tables (e.g. those generated from Google Sheets) to be created by the import routines at runtime.

This behaviour is triggered automatically during import in `login.py`:

```python
# ensure database schemas exist
from db_setup import initialize_all
initialize_all()
```

You can also re-run the initializer anytime to repair a missing table.

Feel free to expand this section when you add new tables or modify existing ones.
