from flask import Flask, render_template, request, redirect, jsonify, send_file, session
import sqlite3
import pandas as pd

app = Flask(__name__)

app.secret_key = "feedback_secret_key"

DATABASE = 'database.db'


# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('index.html')


# =========================
# SUBMIT FEEDBACK
# =========================
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():

    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO feedback(name, email, rating, comments)
        VALUES (?, ?, ?, ?)
    ''', (name, email, rating, comments))

    conn.commit()

    conn.close()

    return redirect('/')


# =========================
# ADMIN LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':

            session['admin'] = True

            return redirect('/admin-dashboard')

    return render_template('login.html')


# =========================
# ADMIN DASHBOARD
# =========================
@app.route('/admin-dashboard')
def admin_dashboard():

    # Check login
    if 'admin' not in session:

        return redirect('/login')

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # Get all feedback
    cursor.execute("SELECT * FROM feedback")

    feedback_data = cursor.fetchall()

    # Total feedback count
    cursor.execute("SELECT COUNT(*) FROM feedback")

    total_feedback = cursor.fetchone()[0]

    # Average rating
    cursor.execute("SELECT AVG(rating) FROM feedback")

    avg_rating = cursor.fetchone()[0]

    # Chart data
    cursor.execute("""
        SELECT rating, COUNT(rating)
        FROM feedback
        GROUP BY rating
    """)

    rating_data = cursor.fetchall()

    conn.close()

    ratings = [str(item[0]) for item in rating_data]

    counts = [item[1] for item in rating_data]

    return render_template(

        'admin.html',

        feedback=feedback_data,

        total_feedback=total_feedback,

        avg_rating=round(avg_rating, 2) if avg_rating else 0,

        ratings=ratings,

        counts=counts
    )


# =========================
# REST API
# =========================
@app.route('/api/feedback')
def api_feedback():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")

    data = cursor.fetchall()

    conn.close()

    return jsonify(data)


# =========================
# EXPORT CSV
# =========================
@app.route('/export-csv')
def export_csv():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql_query(

        "SELECT * FROM feedback",

        conn
    )

    file_name = "feedback_data.csv"

    df.to_csv(file_name, index=False)

    conn.close()

    return send_file(file_name, as_attachment=True)


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/login')


# =========================
# RUN FLASK APP
# =========================
if __name__ == '__main__':

    app.run(debug=True)