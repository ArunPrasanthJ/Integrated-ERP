# Setup Instructions

This document describes the Python packages required by the project and the
steps needed to get the application running on a local machine.

---

## 1. Prepare a virtual environment

It is recommended to create and activate a dedicated Python environment
before installing any packages.  From the project root run:

```bash
python -m venv .venv          # create a venv named ".venv"
# on Windows
.\.venv\Scripts\activate
# on macOS / Linux
source .venv/bin/activate
```

> ⚠️ Make sure you are using Python 3.9+ (the code has been tested with
> 3.10/3.11).  Adjust the `python` command if your system uses a different
> command name (e.g. `python3`).

## 2. Install dependencies

The application relies on the following third‑party libraries which can be
installed with `pip`:

- `Flask` – the web framework
- `Flask-WTF` – form handling and CSRF protection
- `WTForms` – required by Flask-WTF
- `Flask-JWT-Extended` – JWT support used for optional authentication
- `pymysql` – MySQL driver used by some database connections
- `mysql-connector-python` – alternate MySQL driver used by other
  connections (particularly `payments_db` and `hostel_mgmt`)
- `reportlab` – generates PDF receipts for student payments

You can install them all at once:

```bash
pip install Flask Flask-WTF WTForms Flask-JWT-Extended \
            pymysql mysql-connector-python reportlab
```

> 💡 If you prefer to keep a record of installed packages, run
> `pip freeze > requirements.txt` after successful installation.  A
> `requirements.txt` file is not included in this repository by default.

## 3. Database setup

This project uses four MySQL schemas (`test1`, `payments_db`, `details` and
`hostel_mgmt`).  The helper module `db_setup.py` will create all required
databases and tables if they do not already exist.  Before running the
application, ensure MySQL is installed and that the credentials defined in
`db.py`/`db_setup.py` are correct (default user `root` with password
`masterarun1` on `localhost`).

To initialize the databases simply start the Flask app; the very first import
of `login.py` calls `initialize_all()` which invokes the setup functions.

```bash
python login.py
```

You can also manually execute the SQL dump files located in the
`"Data base"` directory if you wish to inspect or recreate the original
table definitions:

```bash
mysql -u root -p < "Data base/payments_db_payments.sql"
```

## 4. Running the server

Once dependencies are installed and MySQL is reachable, launch the app with

```bash
python login.py
```

The development server listens on `http://127.0.0.1:5000/`.  Navigate there in a
browser; the login page will appear.  Default user accounts are not
pre-populated – use the administration interface to add users or insert
records directly into the `test1.users` table.


---

## 5. Additional notes

- Static assets live in the `static/` directory; templates are under
  `templates/`.
- If you make changes to the Python code, restart the server or run it with
  `FLASK_ENV=development flask run` to enable the reloader.
- Credentials and secret keys are currently hard‑coded in `login.py`.  For a
  production deployment you should move them to environment variables or a
  configuration file.

Feel free to adapt these instructions for your environment.