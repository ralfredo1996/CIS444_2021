from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = "BAD PRACTICE BUt IM RUNNING OUT OF TIME"

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['pw'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['pw'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        username = request.form['username']
        password = request.form['password']

        cur = global_db_con.cursor()
        try:
            cur.execute("select password from users where username = %s", (username,))
            row = cur.fetchone()
            db_pw = row[0].encode('ascii')
         
            compare = bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), db_pw)

            print(compare)
        
            if compare == True:
                jwt_str = jwt.encode({"username" : username} , JWT_SECRET, algorithm="HS256")
                return json_response(jwt=jwt_str)
            else:
                return "Record not found", 400
        except:
            return "Record not found", 403

@app.route('/buyBook',  methods=['POST']) #endpoint
def buyBook():
    try:
        data = request.form['jwt']
        jwt.decode(data, JWT_SECRET, algorithms=["HS256"])
    except:
        return "Not allowed" , 403
    username = request.form['username']
    print(username)
    bID = request.form['bookID']
    print(bID)
    cur = global_db_con.cursor()
    cur.execute("select name from books where id = %s", (bID,))
    bookname = cur.fetchone()
    print(bookname)
    cur.execute("insert into purchases (userID, bookID) values (%s, %s)", (username, bookname))
    global_db_con.commit();
    return "Good"
    

@app.route('/books', methods=['GET'])
def books():

    try:
        data = request.args
        token = data["jwt"]
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except:
        return "Not allowed" , 403
    cur = global_db_con.cursor()
    cur.execute("select id, name, price from books;")
    books = cur.fetchall()
    bookArray = []
    for i in books:
        bookArray.append(i)
    return json_response(bookArray=books)

@app.route('/createUser',  methods=['POST']) #endpoint
def createUser():
    username = request.form['username']
    print(username)
    password = request.form['password']
    print(password)
    
    cur = global_db_con.cursor()
    salted = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = (username, salted.decode('ascii'))

    cur.execute(sql, val)
    global_db_con.commit();

    return "Good"

#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/earth') #endpoint
def earth():
        return render_template('client_time.html')

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


app.run(host='0.0.0.0', port=80)

