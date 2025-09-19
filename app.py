from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for flash messages

# -----------------------------
# File Upload Config
# -----------------------------
UPLOAD_FOLDER = "static/uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file is PDF"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Database Connection Function
# -----------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="vasu",          # your MySQL username
            password="root",      # your MySQL password
            database="job_portal"
        )
        return conn
    except Error as e:
        print("Database connection error:", e)
        return None


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY posted_on DESC LIMIT 5")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", jobs=jobs)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        flash("Thank you for contacting us! We will get back to you soon.", "success")
        return redirect("/contact")
    return render_template("contact.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
            flash("✅ Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        except:
            flash("⚠️ Email already exists. Please use another.", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            flash(f"✅ Welcome back, {user['name']}!", "success")
            return redirect(url_for("index"))
        else:
            flash("❌ Invalid email or password!", "danger")
    return render_template("login.html")


@app.route("/job_portal")
def job_portal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY posted_on DESC")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("job_portal.html", jobs=jobs)


@app.route("/post_job", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        title = request.form.get("title")
        company = request.form.get("company")
        location = request.form.get("location")
        description = request.form.get("description")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jobs (title, company, location, description) VALUES (%s, %s, %s, %s)",
            (title, company, location, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("✅ Job posted successfully!", "success")
        return redirect(url_for("job_portal"))
    return render_template("post_job.html")


@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        file = request.files["resume"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Save file path in DB instead of plain text
            cursor.execute(
                "INSERT INTO applications (job_id, name, email, resume) VALUES (%s, %s, %s, %s)",
                (job_id, name, email, file_path)
            )
            conn.commit()
            flash("✅ Application submitted successfully with PDF resume!", "success")
            cursor.close()
            conn.close()
            return redirect(url_for("job_portal"))
        else:
            flash("❌ Invalid file type! Please upload a PDF.", "danger")

    cursor.close()
    conn.close()
    return render_template("apply.html", job=job)


@app.route("/applications")
def applications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id, a.name, a.email, a.resume, a.applied_on,
               j.title AS job_title, j.company AS company
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        ORDER BY a.applied_on DESC
    """)
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("applications.html", applications=applications)


@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword", "")
    location = request.args.get("location", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM jobs
        WHERE title LIKE %s AND location LIKE %s
        ORDER BY posted_on DESC
    """
    cursor.execute(query, (f"%{keyword}%", f"%{location}%"))
    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("search_results.html", jobs=jobs, keyword=keyword, location=location)


if __name__ == "__main__":
    app.run(debug=True)
