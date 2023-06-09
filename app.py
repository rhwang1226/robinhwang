from flask import Flask, render_template, request, g, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
from waitress import serve
import os

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # SQLite database file

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
    languageRows = apiLanguages()
    return render_template("admin.html", languageRows=languageRows)

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


# Run the Flask application
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')