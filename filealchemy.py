from turtle import pd
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, select

hostname = 'localhost'
name = 'mydatabase'
user = 'postgres'
password = '1234'
port = '5432'


engine = db.create_engine('postgresql://postgres:1234@localhost:5432/mydatabase')
conection = engine.connect()
metadata = db.MetaData()
metadata.reflect(bind=engine, only=['project_courses'])
project_courses = metadata.tables['project_courses']
project_courses = db.Table('project_courses', metadata, autoload = True, autoload_with=engine)

print(project_courses.columns.keys())

print(repr(metadata.tables['project_courses']))

query = select(project_courses)
query = select(project_courses.c.course_id, project_courses.c.course_name)


ResultProxy = conection.execute(query)

ResultSet = ResultProxy.fetchall()

ResultSet[:3]

while flag:
    partial_results = ResultProxy.fetchall(50)
    if(partial_results == []):
        flag = False
        pass

ResultProxy.close()

#Dataframe Conversion

df = pd.DataFrame(ResultSet)
df.columns = ResultSet[0].keys()

