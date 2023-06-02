import sqlite3

con = sqlite3.connect('database.db')
print("Connected to database successfully")

#con.execute('DROP TABLE languages')

con.execute('CREATE TABLE languages (name TEXT UNIQUE CHECK(name <> ""), family TEXT NOT NULL, greeting TEXT NOT NULL CHECK(greeting <> ""))')
print("Created table successfully!")

cur = con.cursor()
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Python', 'Programming Language', 'print(\"Hello World\")')")
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Java', 'Programming Language', 'public class HelloWorld {\n\tpublic static void main(string[] args) {\n\t\tSystem.out.println(\"Hello World\");\n\t}\n}')")
cur.execute("INSERT INTO languages (name, family, greeting) VALUES ('Korean', 'Spoken Language', '세상아 안녕')")
con.commit()

con.close()