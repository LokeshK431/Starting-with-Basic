import psycopg2
import psycopg2.extras

hostname = 'localhost'
name = 'mydatabase'
user = 'postgres'
password = '1234'
port = '5432'

conn = None


try:
    with psycopg2.connect(
        host = hostname,
        dbname = name,
        user = user,
        password = password,
        port = port,
    ) as conn:

        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:

            cur.execute('DROP TABLE IF EXISTS employee')

            create_script = ''' CREATE TABLE IF NOT EXISTS employee (
                                    id       int PRIMARY KEY,
                                    name    varchar(40) NOT NULL,
                                    salary  int,
                                    dept_id varchar(30))'''

            cur.execute(create_script)

            insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
            insert_values = [(1, 'Lemon', 10000, 'D1'), (2, 'Tamarind', 12000, 'B5'), (3, 'Almond', 10400, 'F4'), (4, 'Bottle Guard', 10090, 'E3'), (5, 'Spaghetti', 10700, 'Z5')]
            
            for record in insert_values:
                cur.execute(insert_script, record)

            update_script = 'UPDATE employee SET salary = salary + (salary * 0.5)'
            cur.execute(update_script)

            delete_script = 'DELETE FROM employee WHERE name = %s'
            delete_record = ('Almond',)
            cur.execute(delete_script, delete_record)

            cur.execute('SELECT * FROM EMPLOYEE')
            for record in cur.fetchall():
                print(record['name'], record['salary'])

            
    

    

except Exception as error:
    print(error)

finally:
    

    if conn is not None:
        conn.close()

        #with clause will take care of closing the cursor, so there is no specific need to mention to close cursor, as soon as program executes it will automatically close the cursor for us. so cur.close() is not needed. And also the other advantage is commit will also be taken care of. So no need to conn.commit() as soon as the program exists it will commit with no exceptions and if not it will be rolled back. So Database needs to be manually closed. And also cur=None is also not needed.