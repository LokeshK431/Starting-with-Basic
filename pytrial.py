import psycopg2

hostname = 'localhost'
name = 'mydatabase'
user = 'postgres'
password = '1234'
port = '5432'

conn = psycopg2.connect(host = hostname, database = name, user = user, password = password, port = port)
# Open a cursor to perform database operations
cur = conn.cursor()

#View the list of Tables in PostgreSQl Database.
cur.execute("SELECT schemaname, tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema')")
rows = cur.fetchall()
for row in rows:
    print(row)

# Execute a command: create project_courses table

cur.execute("DROP TABLE IF EXISTS project_courses")

cur.execute("""CREATE TABLE project_courses(
            course_id SERIAL PRIMARY KEY,
            course_name VARCHAR (50) UNIQUE NOT NULL,
            course_instructor VARCHAR (100) NOT NULL,
            topic VARCHAR (20) NOT NULL);
            """)


cur.execute("INSERT INTO project_courses(course_name, course_instructor, topic) VALUES('Introduction to SQL','Izzy Weber','Julia')");

cur.execute("INSERT INTO project_courses(course_name, course_instructor, topic) VALUES('Analyzing Survey Data in Python','EbunOluwa Andrew','Python')");

cur.execute("INSERT INTO project_courses(course_name, course_instructor, topic) VALUES('Introduction to ChatGPT','James Chapman','Theory')");

cur.execute("INSERT INTO project_courses(course_name, course_instructor, topic) VALUES('Introduction to Statistics in R','Maggie Matsui','R')");

cur.execute("INSERT INTO project_courses(course_name, course_instructor, topic) VALUES('Hypothesis Testing in Python','James Chapman','Python')");


cur.execute('SELECT * FROM project_courses;')
rows = cur.fetchall()
conn.commit()

for row in rows:
    print(row)

cur.execute("UPDATE project_courses SET topic = 'SQL' WHERE course_name = 'Introduction to SQL'")

cur.execute("""DELETE from project_courses WHERE course_name = 'Introduction to Statistics in R'""");



cur.execute('SELECT * FROM project_courses ORDER BY course_instructor')
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute('SELECT course_instructor, COUNT(*) FROM project_courses GROUP BY course_instructor')
rows = cur.fetchall()
for row in rows:
    print(row)

cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'programming_languages')")
exists = cur.fetchone()[0]

if exists:
    print("The programming_languages table exists.")
else:
    print("The programming_languages table does not exists.")

cur.execute("""CREATE TABLE programming_languages(
            language_id SERIAL PRIMARY KEY,
            language_name VARCHAR (50) NOT NULL,
            language_instructor VARCHAR (50) NOT NULL,
            topic VARCHAR (50) NOT NULL,
            toibe_ranking INT NOT NULL);
""")

#Check if the language_name column exists in programming_languages table.
cur.execute("SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'programming_languages' AND column_name = 'language_name')")
exists = cur.fetchone()[0]
if exists:
    print("The language_name column exists in the programming_language table")
else:
    print("The language_name column does not exist in the programming_languages table")

#Join
cur = conn.cursor()
cur.execute("""SELECT project_courses.course_name, project_courses.course_instructor, project_courses.topic
FROM project_courses
INNER JOIN programming_languages
ON project_courses.topic = programming_languages.language_name""")
rows = cur.fetchall()
for row in rows:
    print(row)

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import text

engine = db.create_engine('postgresql://postgres:1234@localhost:5432/mydatabase')
conn = engine.connect() 
output = conn.execute(text("SELECT * FROM project_courses"))
print(output.fetchall())
conn.close()

# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()