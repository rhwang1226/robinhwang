from flask import Flask, render_template, request, g, jsonify, send_from_directory, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
from waitress import serve
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # SQLite database file
app.config['SECRET_KEY'] = os.environ.get('KEY')

app.static_folder = 'static'

# Define routes and views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/resume')
def resume():
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/resources/'
    return send_from_directory(filepath, 'resume.pdf')

@app.route('/worldofhellos')
def worldOfHellos():
    selectedlanguage = request.args.get('selectedlanguage', default = "python", type = str)
    
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()

    cur.execute("SELECT * FROM languages")

    rows = cur.fetchall()
    languageRows = [{"name": row[0], "family": row[1], "greeting": row[2]} for row in rows]
    

    con.close()
    return render_template("worldofhellos.html",languageRows=languageRows)

@app.route('/robinchronicles')
def robinChronicles():
    return render_template("robinchronicles.html")

@app.route('/api/getblogposts')
def apiBlogPosts():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()

    cur.execute("SELECT * FROM blog")

    rows = cur.fetchall()
    blogPosts = [{"title": row[0], "date": row[1], "text": row[2]} for row in rows]
    
    cur.close()
    con.close()
    return languageRows;

@app.route('/api/getlanguages')
def apiLanguages():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()

    cur.execute("SELECT * FROM languages")

    rows = cur.fetchall()
    languageRows = [{"name": row[0], "family": row[1], "greeting": row[2]} for row in rows]
    
    cur.close()
    con.close()
    return languageRows;

@app.route('/admin')
def admin():
    if 'authenticated' in session:
        languageRows = apiLanguages()
        return render_template("admin.html", languageRows=languageRows)
    
    return login()

@app.route('/admin/addlanguage', methods=['GET','POST'])
def addLanguage():
    if request.method == 'POST':
        langName = request.form.get("langName")
        langFamily = request.form.get("langFamily")
        langGreeting = request.form.get("langGreeting")

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO languages (name,family,greeting) VALUES(?,?,?)", (langName, langFamily, langGreeting))
            con.commit()
        except sqlite3.Error as e:
            print("An error occurred:", e)
        cur.close()
        con.close()

    return admin()

@app.route('/admin/deletelanguage', methods=['GET','DELETE'])
def deleteLanguage():
    langName = request.args.get("langName")
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    try:
        cur.execute("DELETE FROM languages WHERE name = ?", (langName,))
        con.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return jsonify(success=False, message="Error deleting language")

    return admin()

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'authenticated' in session:
        # If the user is already authenticated, redirect to the admin page
        return redirect(url_for('admin'))
    
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # Retrieve the user record from the database
        cur.execute("SELECT password, salt FROM login WHERE username=?", (username,))
        result = cur.fetchone()
        
        if result:
            hashed_password = result[0]
            salt = result[1]
            
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['authenticated'] = True
                return admin()
        
        error = 'Invalid credentials. Please try again.'

    return render_template('adminLogin.html', error=error)



@app.route('/logout')
def logout():
    # Clear the session and log out the user
    session.clear()
    return redirect(url_for('index'))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=5000, url_scheme='https')