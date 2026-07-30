from functools import wraps
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sp"

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads", "archive")
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif", "tiff"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mysql = MySQL(app)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        cursor.execute("SELECT * FROM employees WHERE employee_id=%s", (user["employee_id"],))
        employee = cursor.fetchone()

        if not employee:
            flash("Employee profile not found.", "error")
            return render_template("login.html")

        session["user_id"] = user["username"]
        session["employee_id"] = user["employee_id"]
        session["full_name"] = f"{employee['first_name']} {employee['last_name']}"
        session["office"] = employee["office"]

        office = employee["office"].lower().strip()

        if "procurement" in office:
            session["dashboard_type"] = "archive"
        else:
            session["dashboard_type"] = "requester"

        flash(f"Welcome back, {session['full_name']}!", "success")
        return redirect(url_for("dashboard"))

    except Exception as e:
        print("Database Error:", e)
        flash("An error occurred during login.", "error")
        return render_template("login.html")

    finally:
        cursor.close()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    employee_id = request.form.get("employee_id", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("register.html")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM employees WHERE employee_id=%s", (employee_id,))
        if not cursor.fetchone():
            flash("Invalid Employee ID.", "error")
            return render_template("register.html")

        cursor.execute("SELECT * FROM users WHERE employee_id=%s", (employee_id,))
        if cursor.fetchone():
            flash("Account already exists.", "error")
            return render_template("register.html")

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Username already exists.", "error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, employee_id, password) VALUES (%s, %s, %s)",
            (username, employee_id, hashed_password)
        )

        mysql.connection.commit()
        flash("Account successfully created. Please log in.", "success")
        return redirect(url_for("login"))

    except Exception as e:
        mysql.connection.rollback()
        print("Database Error:", e)
        flash("An error occurred during registration.", "error")

    finally:
        cursor.close()

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    dashboard_type = session.get("dashboard_type")

    if dashboard_type == "archive":
        return render_template("archive/archiveDashboard.html")

    if dashboard_type == "requester":
        return render_template("requester/requesterDashboard.html")

    session.clear()
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)