from flask import Flask, render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import bcrypt

from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
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
