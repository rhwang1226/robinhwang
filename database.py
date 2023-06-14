import sqlite3
import bcrypt

con = sqlite3.connect('database.db')
print("Connected to database successfully")

con.execute('DROP TABLE IF EXISTS languages')
con.execute('DROP TABLE IF EXISTS login')

con.execute('CREATE TABLE languages (name TEXT UNIQUE CHECK(name <> ""), family TEXT NOT NULL, greeting TEXT NOT NULL CHECK(greeting <> ""))')
con.execute('CREATE TABLE login (username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, salt TEXT NOT NULL)')
print("Created table successfully!")

unhashed = "smartbrew87"
salt = bcrypt.gensalt()
password = bcrypt.hashpw(unhashed.encode('utf-8'), salt)
print("Hashed String:", password.decode('utf-8'))

cur = con.cursor()
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Python', 'Programming Language', 'print(\"Hello World\")')")
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Java', 'Programming Language', 'public class HelloWorld {\n\tpublic static void main(string[] args) {\n\t\tSystem.out.println(\"Hello World\");\n\t}\n}')")
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Korean', 'Spoken Language', '세상아 안녕')")

cur.execute("INSERT INTO login (username, password, salt) VALUES ('admin', '" + str(password.decode()) + "', '" + str(salt.decode()) + "')")
con.commit()

con.close()