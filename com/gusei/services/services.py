from com.gusei.dao.Dao import Dao
from com.gusei.admin_panel.user.User import User
from com.gusei.services.crypt import Crypt
from com.gusei.dbConnections.DbConnection import DbConnection
import com.gusei.DefinePaths.Logger as logger
import random
import string
import re
from werkzeug.utils import secure_filename
from com.gusei.DefinePaths.DefinePaths import DefinePath
from com.gusei.controller.constants.read_constants import ReadConstants
from com.gusei.utils.utils import Utils
from com.gusei.music.music import Music
import json
import os
from flask import request

karaoke_folder_path=DefinePath.get_karaoke_folder_path()
ALLOWED_EXTENSIONS = {'mp3', 'wave'}
crypt = Crypt()
log = logger.get_logger()
users_collection = "users"
deployment_collection = "script_config"
org_collection = "organisations"
# excelFilesPath = DefinePath.getxlsxpath()
messages = ReadConstants()
message_dict = messages.get_constant_object('response_messages_list.properties', 'Response_messages')
config_dic = messages.get_constant_object('response_messages_list.properties', 'Schedule_configuration')



class Service:

    def __init__(self):
        self.dao = Dao()
        self.utl = Utils()
        self.user=User()
        self.mu = Music()
        # self.ist_dt = self.utl.get_ist_time()

    def insert_user_info(self,content,id=None):
        fname = str(content.get("first_name")).strip()
        lname = str(content.get("last_name")).strip()
        email = str(content.get("user_email")).strip()
        password = str(content.get("password")).strip()
        social_type = str(content.get("social_type")).strip()
        social_id = str(content.get("social_id")).strip()
        phone_no = str(content.get("phone_no")).strip()
        role = str(content.get("role")).strip()
        reg_date = self.utl.get_current_datetime()
        update_date = self.utl.get_current_datetime()
        status,message=self.validation_signup(fname,lname,email,password,phone_no,role)
        if status=="success":
            social_type_list=[]
            social_id_list=[]
            crypt_password = crypt.encrypt(password)
            social_type_list, social_id_list = self.dao.get_social_type_and_id_list(email,"user_registered")
            if len(social_type_list)==0 and len(social_id_list)==0:
                if social_type.lower() in ['manual','facebook','google']:
                    social_type_list.append(social_type.lower())
                    print(social_type_list)
                    if social_id != "":
                        social_id_list.append(social_id)
                else:
                    return "Failed", "Invalid Signup",
                social_type_list = set(social_type_list)
                social_id_list = set(social_id_list)
                social_type_set = json.dumps(list(social_type_list))
                social_id_set = json.dumps(list(social_id_list))
                status, message = self.dao.insert_signup_data(fname,lname,email,crypt_password,social_type_set,
                                                              social_id_set,id,phone_no,role,reg_date,
                                                              update_date,"user_registered")
            else:
                status, message = self.dao.insert_signup_data(fname, lname, email, crypt_password, social_type,
                                                              social_id,id, phone_no, role, reg_date,
                                                              update_date, "user_registered")

            return status, message
        else:
            return status, message

    def update_user_info(self, content,user_id):
        fname = str(content.get("first_name")).strip()
        lname = str(content.get("last_name")).strip()
        phone_no = str(content.get("phone_no")).strip()
        update_date = self.utl.get_current_datetime()
        status, message = self.validation_update(fname, lname, phone_no)
        if status == "success":
            status, message = self.dao.insert_update_data(fname, lname, phone_no,user_id, update_date,
                                                          "user_registered")
            return status, message
        else:
            return status, message


    def validation_update(self,fname,lname,phone_no):
        fname_status, message = self.validate_input_value_is_empty(fname)
        if fname_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        lname_status, message = self.validate_input_value_is_empty(lname)
        if lname_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        phone_status, message = self.validate_input_value_is_empty(phone_no)
        if phone_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        return "success",""

    def validation_signup(self,fname,lname,email,password,phone_no,role):
        fname_status, message = self.validate_input_value_is_empty(fname)
        if fname_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        lname_status, message = self.validate_input_value_is_empty(lname)
        if lname_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        email_status, message = self.validate_input_value_is_empty(email)
        if email_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        email_validate_status, message=self.validationForMail(email)
        if email_validate_status != "success":
            return "Failed", message
        # password_status, message = self.validate_input_value_is_empty(password)
        # if password_status != "success":
        #     return "Failed", message_dict.get('invalid_signup')
        # medium_status, message = self.validate_input_value_is_empty(medium)
        # if medium_status != "success":
            # return "Failed", message_dict.get('invalid_signup')
        phone_status, message = self.validate_input_value_is_empty(phone_no)
        if phone_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        role_status, message = self.validate_input_value_is_empty(role)
        if role_status != "success":
            return "Failed", message_dict.get('invalid_signup')
        return "success",""

    def validate_input_value_is_empty(self, value):
        try:
            if value is not None and value != "" and value != "None":
                return "success", value
            else:
                return "failed", "Mandatory field! Can not be empty."
        except Exception as e:
            log.error(str(e))
            return "failed", str(e)

    def validateUser(self,content):
        social_type=str(content.get("social_type")).strip()
        if social_type.lower() in ['manual','facebook', 'google']:
            if social_type=="manual":
                email = str(content.get("user_email")).strip()
                password = str(content.get("password")).strip()
                if email is None or email == "" or password is None or password == "":
                    return "Failed"
                status,pwdFrmDb,sessions,ip = self.dao.findUserByEmail(email, 'user_login')
                if status == "Failed":
                    return "Failed"
                deCryptPswdcrypt = crypt.decrypt(pwdFrmDb)
                if password != deCryptPswdcrypt:
                    return "Failed"
            if social_type=="facebook" or social_type=="google":
                email = str(content.get("user_email")).strip()
                social_id=str(content.get("social_id")).strip()
                if email is None or email == "" or social_id is None or social_id == "":
                    return "Failed"
                status,social_id_list,sessions,ip = self.dao.findUserByEmailSocial(email, 'user_login')
                if status == "Failed":
                    # redirect to signup
                    return "Failed"
                if social_id not in social_id_list:
                    return "Failed"
            session_list=json.loads(sessions)
            session_id=self.gen_session()
            session_list.append(session_id)
            session_list=json.dumps(session_list)
            ip_list=json.loads(ip)
            ip_id=request.remote_addr
            ip_list.append(ip_id)
            ip_list=json.dumps(ip_list)
            return self.dao.updateSessionIp(session_list,ip_list, email, 'user_login'),session_id
        return "Failed"

    def validateSession(self, sessionId,email,ip_add):
        return self.dao.validateSession(sessionId,email,ip_add,'user_login')

    def logoutUser(self, sessionID,email,ip_add):
        return self.dao.logoutUser(sessionID,email,ip_add, 'user_login')

    def get_user_by_SessionID(self, sessionID):
        return self.dao.get_user_by_SessionID(sessionID, users_collection)

    def gen_session(self):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(20)]
        return ("".join(keylist))

    def update_deployment_data(self, user_id, data):
        return self.dao.update_deployment_data(data, user_id, deployment_collection)

    def validationForMail(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            return "success", email
        else:
            return "failed", message_dict.get('incorrect_email_address')

    def create_Otp(self):
        return random.randint(1000, 9999)

    def admin_insert_user_info(self, content, user_id):
        fname = str(content.get("first_name")).strip()
        lname = str(content.get("last_name")).strip()
        email = str(content.get("user_email")).strip()
        password = str(content.get("password")).strip()
        social_type = str(content.get("social_type")).strip()
        social_id = str(content.get("social_id")).strip()
        phone_no = str(content.get("phone_no")).strip()
        role = str(content.get("role")).strip()
        created_by = str(user_id),
        reg_date = self.utl.get_current_datetime()
        update_date = self.utl.get_current_datetime()
        status, message = self.validation_signup(fname, lname, email, password, phone_no, role)
        if status == "success":
            crypt_password = crypt.encrypt(password)
            status, message = self.user.insert_signup_data(fname, lname, email, crypt_password, social_type, social_id,
                                                          phone_no, role, created_by, reg_date, update_date,
                                                          "user_registered")
            return status, message, email
        else:
            return status, message

    def admin_update_user_info(self, content,user_id,id):
        fname = str(content.get("first_name")).strip()
        lname = str(content.get("last_name")).strip()
        phone_no = str(content.get("phone_no")).strip()
        update_date = self.utl.get_current_datetime()
        status, message = self.validation_update(fname, lname, phone_no)
        if status == "success":
            status, message = self.user.insert_update_data(fname, lname, phone_no,user_id, update_date,
                                                          id,"user_registered")
            return status, message
        else:
            return status, message


    def get_id_by_email(self,email):
        query_string = "select ID from user_login  where user_email = %(email)s"
        connection = DbConnection.getDbConnection()
        cursor = connection.cursor()
        cursor.execute(query_string, {"email": email})
        user_query = cursor.fetchall()
        id = user_query[0]
        user_id=str(id.get("ID"))
        return user_id

    def deleteUser(self,id,user_id):
        status,messages=self.user.deleteUser(id,user_id,"user_registered","user_login")
        return status , messages

    def follow(self,id,user_id):
        status,messages=self.dao.follow(id,user_id,"follow")
        return status,messages

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def karaoke_uploader(self,path,file,email):
        try:
            if self.allowed_file(file.filename):
                original_filename = secure_filename(file.filename)
                filename=self.create_filename(original_filename)
                file.save(path+"/"+filename)
                user_id = self.get_id_by_email(email)
                duration=self.mu.get_file_duration(path+"/"+filename)
                status, message, data,audio_id= self.dao.insert_karaoke(filename,original_filename,user_id,duration)
                if status == "success" and len(data)>0:
                    original_filename=data[0]['original_filename']
                    karaoke_filename= data[0]['karaoke_filename']
                    duration=data[0]['duration']
                    url=re.split('(http://|ftp://|https://)?[^/\?]*$',request.base_url)[0]
                    file_url=str(url)+"karaoke/"+str(karaoke_filename)
                    return "success", message,file_url,original_filename,audio_id,duration
                else:
                    log.error("Exception occur when inserting db." + message)
                    return "Failed", "Something went wrong","","","",""
            else:
                return "Failed", "Please upload the correct format. We are accepting only (mp3,wave).","","",""
        except Exception as e:
            log.exception("")
            log.error("Exception occur when uploading karaoke " + str(e))
            return "Failed", "Something Went wrong Please check the error logs.","","","",""

    def blockUser(self, id, user_id):
        status, messages = self.user.blockUser(id, user_id, "user_login")
        return status, messages

    def create_filename(self,filename):
        timestamp=self.utl.get_current_datetime_str()
        filename=filename.split(".")
        ext=filename[1]
        name=filename[0]
        timestamp=timestamp.replace(":","").replace(" ","").replace("-","")
        filename=str(name)+"_"+str(timestamp)+str(random.randint(1000, 9999))+"."+str(ext)
        return filename

    def get_follower_list(self, id, user_id):
        status, data = self.dao.get_follower_list(id, user_id, "follow")
        return status, data

    def get_following_list(self, id, user_id):
        status, data = self.dao.get_following_list(id, user_id, "follow")
        return status, data

    def insert_song_data(self,song_details,user_id):
        status, message = self.dao.insert_song_data(song_details,user_id)
        return status,message

    def get_song_data(self,user_id):
        status, message,data = self.dao.get_song_data(user_id)
        return status,message,data
    
    def authorize_karaoke(self,id):
        status,messages=self.dao.authorize_karaoke(id,"songs")
        return status , messages

    def delete_karaoke(self,id):
        status,messages=self.dao.delete_karaoke(id,"karaoke","songs")
        return status , messages
    
    def update_song_data(self,song_details,user_id,id):
        status, message = self.dao.update_song_data(song_details,user_id,id,"songs")
        return status,message
    
    def user_list(self):
        status, data = self.user.user_list("user_registered")
        return status,data
    
    def user_details(self,id):
        status, data = self.user.user_details(id,"user_registered")
        return status,data