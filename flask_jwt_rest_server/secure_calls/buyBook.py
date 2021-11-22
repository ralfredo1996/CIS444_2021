from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
from tools.logging import logger

global_db_con = get_db()

def handle_request():
    logger.debug("Buy Books handle request")
    print(request.args.getlist('username')[0])
    username = request.args.getlist('username')[0]
    print(username)
    bID = request.args.getlist('bookID')[0]
    print(bID)
    cur = global_db_con.cursor()
    cur.execute("select name from books where id = %s", (bID,))
    bookname = cur.fetchone()
    print(bookname)
    cur.execute("insert into purchases (userID, bookID) values (%s, %s)", (username, bookname))
    global_db_con.commit();
    return "Good"
