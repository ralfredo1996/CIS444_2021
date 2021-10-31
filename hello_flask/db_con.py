import psycopg2
import bcrypt

def get_db():
    return psycopg2.connect(host="localhost", dbname="books" , user="superuser", password="Thanosdidnothingwrong1!")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 



if __name__ == "__main__":
    db, cur = get_db_instance()

    pw = "myspace"
    salted = bcrypt.hashpw(bytes(pw, 'utf-8'),  bcrypt.gensalt(12))
    print(salted)
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    
    val = ("Tom", salted.decode('ascii'))
    print(type(salted))
    cur.execute(sql, val)
    db.commit()

    #cur.execute("select * from users")
    #for r in cur.fetchall():
        #print(r)


