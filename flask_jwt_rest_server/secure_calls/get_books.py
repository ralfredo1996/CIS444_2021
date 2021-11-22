from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
from tools.logging import logger

global_db_con = get_db()

def handle_request():
    logger.debug("Get Books Handle Request")
    cur = global_db_con.cursor()
    cur.execute("select id, name, price from books;")
    books = cur.fetchall()
    bookArray = []
    for i in books:
        bookArray.append(i)
    return json_response( token = create_token(  g.jwt_data ) , bookArray=books)


