from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger
from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    username_from_user_form = request.form['firstname']
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['firstname'] 
            }
    print(user)
    print(password_from_user_form)

    
    cur = global_db_con.cursor()

    try:
        cur.execute("select password from users where username = %s", (username_from_user_form, ))
        row = cur.fetchone()
        db_pw = row[0].encode('ascii')

        compare = bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), db_pw)
        
        if compare == True:
            return json_response( token = create_token(user), authenticated = True)

    except:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    

