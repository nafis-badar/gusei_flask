from flask import Flask,send_from_directory
from flask import request
from com.gusei.dbConnections.DbConnection import DbConnection
from com.gusei.utils.utils import Utils
from com.gusei.services.services import Service
from flask_cors import CORS, cross_origin
import codecs
from com.gusei.DefinePaths.DefinePaths import DefinePath
from com.gusei.controller.constants.read_constants import ReadConstants
import com.gusei.DefinePaths.Logger as logger
import json


service = Service()
defined_path = DefinePath()
log = logger.get_logger()
messages = ReadConstants()
message_dict = messages.get_constant_object('response_messages_list.properties', 'Response_messages')
config_dic = messages.get_constant_object('response_messages_list.properties', 'Schedule_configuration')
codecs.register_error("strict", codecs.ignore_errors)
app = Flask(__name__)
karaoke_folder_path=DefinePath.get_karaoke_folder_path()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Credentials'] = True
connection = DbConnection.getDbConnection()
utl = Utils()
puplic_domain_list=config_dic.get('puplic_domain_list').split(' ')


def validateSession(sessionId,email,ip_add):
    if service.validateSession(sessionId,email,ip_add) is None:
        return None, None, None
    else:
        return sessionId,email,ip_add

@app.route("/")
def index():
    return "hello world"


@app.route("/signup", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def user_singup():
    content = request.json
    try:
        status,message =service.insert_user_info(content)
        if status == "success":
            if status == "success":
                return {"message": "Signup successfully", "status": status}, 200
            else:
                return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
        else:
            return {"message": message, "status": "Failed"}, 400
    except Exception as e:
        log.exception("")
        log.error("Exception While user signup " + str(e))
        return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/update", methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def update_user():
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        content = request.json
        try:
            user_id = service.get_id_by_email(email)
            status, message = service.update_user_info(content,user_id)
            if status == "success":
                if status == "success":
                    return {"message": "Please enter the OTP sent on your email-id.", "status": status,
                            "email": email}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"message": message, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/login", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def login():
    try:
        content = request.json
        status, session_id = service.validateUser(content)
        # print(status,session_id)
        if status == "success":
            return {"session_id": session_id,"status": "success", "message":"login successfully"}, 200
        else:
            return {"message": "Invalid Username or password", "status": "Failed"}, 400
    except Exception as e:
        log.exception("")
        log.error("Exception While login "+str(e))
        return {"message": "Something went wrong", "status": "Failed"}, 400


@app.route("/logout", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def logout():
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    status = service.logoutUser(sessionID,email,ip_add)
    if status == "success":
        return {"message": message_dict.get('successful_logout'), "status": 200}, 200
    else:
        return {"message": message_dict.get('invalid_request'), "status": 400}, 400


@app.route("/admin/user/create", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def admin_create_user():
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        content = request.json
        try:
            user_id=service.get_id_by_email(email)
            status, message, email = service.admin_insert_user_info(content,user_id)
            if status == "success":
                if status == "success":
                    return {"message": "User created.", "status": status,
                            "email": email}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"message": message, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/admin/user/update/<int:id>", methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def admin_update_user(id):
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        content = request.json
        try:
            user_id=service.get_id_by_email(email)
            id=id
            status, message = service.admin_update_user_info(content,user_id,id)
            if status == "success":
                if status == "success":
                    return {"message": "User updated.", "status": status,
                            "email": email}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"message": message, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/admin/user/delete/<int:id>", methods=['DELETE'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def delete(id):
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if (sessionID is None or len(sessionID) == 0):
        return {"message": "invalid request", "status": "error"}, 401
    user_id = service.get_id_by_email(email)
    status,messages = service.deleteUser(id,user_id)
    if (status == "success"):
        return {"message": messages, "status": 200}, 200
    else:
        return {"message": messages, "status": 400}, 400


@app.route("/follow/<int:id>", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def follow(id):
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        try:
            user_id = service.get_id_by_email(email)
            status, message = service.follow(user_id, id)
            if status == "success":
                if status == "success":
                    return {"message": message, "status": status,
                            "email": email}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"message": message, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/upload_karaoke", methods=['post'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def upload_karaoke():
    try:
        sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),request.remote_addr)
        if sessionID is None or len(sessionID) == 0 or email is None or len(email) == 0:
            return {"message": "invalid request", "status": "error"}, 401
        file=request.files['karaoke']
        if file is not None:
            if file.filename == '':
                return {"message": "invalid request", "status": "error"}, 401
            else:
                status,message,file_url,filename,audio_id,duration=service.karaoke_uploader(karaoke_folder_path,file,email)
                if status == "success":
                    return {"message": str(message),"audio_id":audio_id,"audio_url":file_url,"filename":filename,"duration":duration+"s","status": 200}, 200
                else:
                    return {"message": str(message), "status": 400}, 400
        else:
            return {"message": "something went wrong", "status": 400}, 400
    except Exception as e:
        log.exception("")
        log.error("Exception While upload karaoke "+ str(e))
        return {"message": "something went wrong", "status": 400}, 400

@app.route("/karaoke/<filename>", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_file(filename):
    try:
        sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),request.remote_addr)
        if sessionID is None or len(sessionID) == 0 or email is None or len(email) == 0:
            return {"message": "invalid request", "status": "error"}, 401
        else:
            return send_from_directory(karaoke_folder_path,filename),200

    except Exception as e:
        log.exception("")
        log.error("Exception While upload karaoke "+ str(e))
        return {"message": "something went wrong", "status": 400}, 400


@app.route("/admin/user/block/<int:id>", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def block(id):
    sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),
                                               request.remote_addr)
    if (sessionID is None or len(sessionID) == 0):
        return {"message": "invalid request", "status": "error"}, 401
    user_id = service.get_id_by_email(email)
    status,messages = service.blockUser(id,user_id)
    print(status)
    if (status == "success"):
        return {"message": str(messages), "status": 200}, 200
    else:
        return {"message": messages, "status": 400}, 400

@app.route("/follower_list/<int:id>", methods=['GET'])
@app.route("/follower_list", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def follower_list(id=None):
    sessionID, email,ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),str(request.remote_addr))
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        try:
            user_id = service.get_id_by_email(email)
            status,data= service.get_follower_list(id, user_id)
            if status == "success":
                if status == "success":
                    return {"Data": data, "status": status}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"data": data, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400


@app.route("/following_list/<int:id>", methods=['GET'])
@app.route("/following_list", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def following_list(id=None):
    sessionID, email,ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),request.remote_addr)
    if sessionID is None or len(sessionID) == 0:
        return {"message": "invalid request", "status": "error"}, 401
    else:
        try:
            user_id = service.get_id_by_email(email)
            status,data= service.get_following_list(id, user_id)
            if status == "success":
                if status == "success":
                    return {"Data": data, "status": status}, 200
                else:
                    return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400
            else:
                return {"data": data, "status": "Failed"}, 400
        except Exception as e:
            log.exception("")
            log.error("Exception While user signup " + str(e))
            return {"message": message_dict.get('exception_error'), "status": "Failed"}, 400

@app.route("/upload_song_details", methods=['post'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def upload_song_detail():
    try:
        sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),request.remote_addr)
        if sessionID is None or len(sessionID) == 0 or email is None or len(email) == 0:
            return {"message": "invalid request", "status": "error"}, 401
        json_data=request.json
        if json_data is not None:
            user_id = service.get_id_by_email(email)
            status, message=service.insert_song_data(json_data,user_id)
            if status=="success":
                return {"message": "successfully uploaded","status":200}, 200
            else:
                return {"message": "something went wrong","status":400}, 400
        else:
            return {"message": "invalid request", "status": "error"}, 401
    except Exception as e:
        log.exception("")
        log.error("Exception While upload karaoke "+ str(e))
        return {"message": "something went wrong", "status": 400}, 400


@app.route("/get_song_details", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_songs_detail():
    try:
        sessionID, email, ip_add = validateSession(request.headers.get('session'), request.headers.get('email'),request.remote_addr)
        if sessionID is None or len(sessionID) == 0 or email is None or len(email) == 0:
            return {"message": "invalid request", "status": "error"}, 401

        user_id = service.get_id_by_email(email)
        status, message, data = service.get_song_data(user_id)
        if status == "success":
            return {"message": "successfully uploaded","song_details":data,"status": 200}, 200
        else:
            return {"message": "something went wrong", "status": 400}, 400

    except Exception as e:
        log.exception("")
        log.error("Exception While upload karaoke " + str(e))
        return {"message": "something went wrong", "status": 400}, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
