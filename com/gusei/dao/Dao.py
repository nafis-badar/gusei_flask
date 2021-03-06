from com.gusei.dbConnections.DbConnection import DbConnection
import json


class Dao:

    def insert_signup_data(self, fname, lname, email, password,social_type,social_id,id, phone_no, role,reg_date, update_date,
                           table_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(table_name) + " where user_email =%(email)s"
            cursor.execute(query_string,{"email":email})
            is_email_exists = cursor.fetchall()
            if is_email_exists is not None and len(is_email_exists) > 0:

                social_type_list, social_id_list = self.get_social_type_and_id_list(email, "user_registered")

                if (len(social_type_list)==3 and len(social_id_list)==2) or social_type.lower() in social_type_list:
                    return "Failed", "Email Id already existed, Please try login"
                else:

                    manual=None
                    if social_type.lower() in ['manual','facebook', 'google']:
                        if social_type=="manual":
                            manual=social_type
                        social_type_list.append(social_type.lower())
                        if social_id != "":
                            social_id_list.append(social_id)
                    else:
                        return "Failed", "Invalid Signup",

                    social_type_list = set(social_type_list)
                    social_id_list = set(social_id_list)
                    social_type_set = json.dumps(list(social_type_list))
                    social_id_set = json.dumps(list(social_id_list))

                    if manual is None:
                        query_update_string= "UPDATE " + str(table_name) + " SET social_type = %(social_type_set)s,social_id=%(social_id_set)s" \
                                                               " WHERE user_email =%(email)s"
                        print(query_update_string)
                        cursor.execute(query_update_string,
                                       {"social_type_set": social_type_set, "social_id_set": social_id_set,"email":email})
                        query_update_string = "UPDATE user_login SET social_type = %(social_type_set)s,social_id=%(social_id_set)s" \
                                          " WHERE user_email =%(email)s"
                        cursor.execute(query_update_string,
                                       {"social_type_set": social_type_set, "social_id_set": social_id_set,
                                        "email": email})
                    else:
                        query_update_string = "UPDATE user_login SET password=%(password)s,social_type=%(social_type_set)s WHERE user_email =%(email)s"
                        cursor.execute(query_update_string,{"password": password,"email":email,'social_type_set':social_type_set})

                        query_update_string = "UPDATE " + str(
                            table_name) + " SET social_type = %(social_type_set)s WHERE user_email =%(email)s"
                        cursor.execute(query_update_string,
                                       {"social_type_set": social_type_set,"email": email})
                    cursor.close()
                    connection.commit()
                    return "success","signup successfully"
            query_signup_string = "INSERT INTO " + str(
                table_name) + "(first_name, last_name, user_email, social_type,social_id, phone_no, role," \
                            "registration_date,updated_date,is_deleted) VALUES (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s)"
            cursor.execute(query_signup_string,(fname,lname,email,social_type,social_id,phone_no,role,
                                                reg_date,update_date,0))
            query_login_string = "INSERT INTO user_login (role,user_email, password,social_type,social_id,\
            session_list,ip_list,is_deleted) VALUES (%s, %s,%s, %s,%s,%s,%s,%s)"
            cursor.execute(query_login_string,(role,email,password,social_type,social_id,"[]","[]",0))
            cursor.close()
            connection.commit()
            return "success", "User has been added successfully"

        except Exception as e:
            print(e)
            return "Failed", "Something went wrong"
        finally:
            if connection is not None:
                connection.close()

    def insert_update_data(self, fname, lname, phone_no, user_id, update_date,
                           table_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()

            query_string = "select * from " + str(table_name) + " where ID =%(user_id)s AND is_deleted=0"
            cursor.execute(query_string, {"user_id": user_id})
            # query_update_string = "INSERT INTO " + str(
            #     table_name) + "(first_name, last_name, phone_no, updated_date,is_deleted) VALUES ( %s,%s,%s,%s,%s)"

            # query_update_string = "UPDATE " + str(table_name) + " SET " + "(first_name, last_name, phone_no, updated_date)" \
            #     " VALUES ( %s,%s,%s,%s)" + " WHERE '" + str(table_name) + "'.'ID'=" + str(user_id)

            # query_update_string = "UPDATE " + str(table_name) + "SET "+"( first_name =% s, last_name =% s, phone_no =% s, updated_date =% s)" + " WHERE ID = "+str(user_id)

            query_update_string = "UPDATE " + table_name + " SET first_name =%(fname)s,last_name='" + str(
                lname) + "',phone_no='" + str(phone_no) + "',updated_date='" + str(
                update_date) + "' WHERE ID = " + user_id

            print(query_update_string)
            # cursor.execute(query_update_string,(y_ufname,lname,phone_no,update_date))
            cursor.execute(query_update_string, {"fname": fname})
            cursor.close()
            connection.commit()
            return "success", "User has been updated successfully"

        except Exception as e:
            print(e)
            return "Failed", "Something went wrong"
        finally:
            if connection is not None:
                connection.close()

    def findUserByEmail(self, email, tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_email = %(email)s and is_blocked=0 and is_deleted=0"
            cursor.execute(query_string, {"email": email})
            is_email_exists = cursor.fetchall()
            print(email)
            print(is_email_exists)
            if is_email_exists is not None and len(is_email_exists) > 0:
                return "success", is_email_exists[0]['password'], is_email_exists[0]['session_list'],is_email_exists[0]['ip_list']
            else:
                return "Failed", "Email id does not Exist", ""
        except Exception as e:
            print(e)
            return "Failed", "Something went wrong", ""
        finally:
            if connection is not None:
                connection.close()

    def findUserByEmailSocial(self, email, tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_email = %(email)s"
            cursor.execute(query_string, {"email": email})
            is_email_exists = cursor.fetchall()
            if is_email_exists is not None and len(is_email_exists) > 0:
                return "success", is_email_exists[0]['social_id'], is_email_exists[0]['session_list'],is_email_exists[0]['ip_list']
            else:
                return "Failed", "Email id does not Exist", ""
        except Exception as e:
            print(e)
            return "Failed", "Something went wrong", ""
        finally:
            if connection is not None:
                connection.close()

    def get_social_type_and_id_list(self, email, table_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()

            query_string = "select * from " + str(table_name) + " where user_email =%(email)s"
            cursor.execute(query_string, {"email": email})
            email_data = cursor.fetchall()
            cursor.close()
            if email_data is not None and len(email_data) > 0:
                return json.loads(email_data[0]['social_type']), json.loads(email_data[0]['social_id'])
            else:
                return [], []

        except Exception as e:
            print(e)
            return [], []
        finally:
            if connection is not None:
                connection.close()

    def updateSessionIp(self, session_list,ip_list, email, tb_name):
        connection = None
        print(session_list,ip_list)
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_login_string = "UPDATE " + str(
                tb_name) + " SET session_list = %(session_list)s ,ip_list=%(ip_list)s WHERE user_email =%(email)s"
            cursor.execute(query_login_string, {"session_list": session_list,"ip_list":ip_list, "email": email})
            print(query_login_string)
            cursor.close()
            connection.commit()
            return "success"
        except Exception as e:
            print(e)
            return "Failed"
        finally:
            if connection is not None:
                connection.close()

    def validateSession(self, sessionId, email,ip_add, tb_name):
        connection = None
        try:

            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_email = %(email)s"
            cursor.execute(query_string, {"email": email})
            data = cursor.fetchall()

            if data is not None and len(data) > 0:
                sessions = data[0]['session_list']
                session_list = json.loads(sessions)
                ip=data[0]['ip_list']
                ip_list = json.loads(ip)
                print(ip_list)
                if sessionId in session_list:
                    if ip_add in ip_list:
                        return "success"
                    else:
                        return None
                else:
                    return None
            else:
                return None

        except Exception as e:
            print(e)
            return None
        finally:
            if connection is not None:
                connection.close()

    def logoutUser(self, sessionID, email,ip_add, tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_email = %(email)s"
            cursor.execute(query_string, {"email": email})
            data = cursor.fetchall()
            if data is not None and len(data) > 0:
                session_list = []
                sessions = data[0]['session_list']
                session_list = json.loads(sessions)
                ip_list=[]
                ip=data[0]['ip_list']
                ip_list = json.loads(ip)
                if sessionID in session_list and ip_add in ip_list:
                    session_list.remove(sessionID)
                    ip_list.remove(ip_add)
                    print(session_list,ip_list)
                    # query_login_string = "UPDATE " + tb_name + " SET session_list = %(session_list)s WHERE user_email = %(email)s"
                    query_login_string = "UPDATE " + str(tb_name) + " SET session_list = %(session_list)s ,ip_list=%(ip_list)s WHERE user_email =%(email)s"
                    cursor.execute(query_login_string, {"session_list": json.dumps(session_list),"ip_list": json.dumps(ip_list), "email": email})
                    cursor.close()
                    connection.commit()
                    return "success"
                else:
                    return None
        except Exception as e:
            print(e)
            return "Failed"
        finally:
            if connection is not None:
                connection.close()

    def follow(self, id, user_id, tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_id=" + str(
                user_id) + " and following_user_id=" + id
            cursor.execute(query_string)
            data = cursor.fetchall()
            if data is not None and len(data) > 0:
                data1 = data[0]['is_unfollow']
                if data1 == 0:
                    query_unfollow_update_string = "UPDATE " + str(
                        tb_name) + " SET `is_unfollow` = '1' WHERE user_id=" + str(
                        user_id) + " and following_user_id=" + id
                    cursor.execute(query_unfollow_update_string)
                    cursor.close()
                    connection.commit()
                    return "success", "unfollowed"
                if data1 == 1:
                    query_follow_update_string = "UPDATE " + str(
                        tb_name) + " SET `is_unfollow` = '0' WHERE user_id=" + str(
                        user_id) + " and following_user_id=" + id
                    cursor.execute(query_follow_update_string)
                    cursor.close()
                    connection.commit()
                    return "success", "followed"
                else:
                    return "failed", "something in not in tone"
            else:
                query_follow_string = "INSERT INTO " + str(
                    tb_name) + "(user_id,following_user_id) VALUES (%s, %s)"

                print(query_follow_string)
                cursor.execute(query_follow_string, (user_id, id))
                cursor.close()
                connection.commit()
                # cursor.execute(query_string, {"email": email})
                # data = cursor.fetchall()
                return "success", "followed"
        except Exception as e:
            print(e)
            return None
        finally:
            if connection is not None:
                connection.close()

    def insert_karaoke(self,filename,original_filename,user_id,duration):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_karaoke_string = "INSERT INTO karaoke(user_id, karaoke_filename,original_filename,duration,is_confirm,is_deleted) " \
                                  "VALUES (%s, %s, %s,%s, %s, %s)"
            cursor.execute(query_karaoke_string, (user_id, filename,original_filename,duration,0,0))
            last_id=cursor.lastrowid
            get_karaoke = "Select original_filename, karaoke_filename,duration from karaoke Where ID=%(id)s"
            cursor.execute(get_karaoke, {"id":last_id})
            data=cursor.fetchall()

            connection.commit()
            cursor.close()
            return "success", "Successfully uploaded",data,last_id
        except Exception as e:
            return "Failed", "Something went wrong" + str(e),[],""
        finally:
            if connection is not None:
                connection.close()

    def get_follower_list(self,id,user_id,tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            print(id)
            print(user_id)
            if id is not None:
                # query_string= "select * from " + str(tb_name) + " where user_id=" + str(id) + " and is_unfollow=0"
                query_string= "select * from " + str(tb_name) + " where user_id=%(id)s and is_unfollow=0"
                print(query_string)
                cursor.execute(query_string,{"id":id})
                data = cursor.fetchall()
                return "success",data
            if id is None:
                # query_string= "select * from " + str(tb_name) + " where user_id=" + str(user_id) + " and is_unfollow=0"
                query_string= "select * from " + str(tb_name) + " where user_id=%(user_id)s and is_unfollow=0"
                print(cursor.execute(query_string,{"user_id":str(user_id)}))
                data = cursor.fetchall()
                return "success",data
            else:
                return "Failed","data not found"
        except Exception as e:
            return "Failed", "Something went wrong" + str(e)
        finally:
            if connection is not None:
                connection.close()

    def get_following_list(self,id,user_id,tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            print(id)
            print(user_id)
            if id is not None:
                query_string= "select * from " + str(tb_name) + " where following_user_id=%(id)s and is_unfollow=0"
                print(query_string)
                cursor.execute(query_string,{"id":id})
                data = cursor.fetchall()
                return "success",data
            if id is None:
                query_string= "select * from " + str(tb_name) + " where following_user_id=%(user_id)s and is_unfollow=0"
                print(query_string)
                cursor.execute(query_string,{"user_id":str(user_id)})
                data = cursor.fetchall()
                return "success",data
            else:
                return "Failed","data not found"
        except Exception as e:
            return "Failed", "Something went wrong" + str(e)
        finally:
            if connection is not None:
                connection.close()

    def insert_song_data(self,song_details,user_id):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()

            query = "INSERT INTO songs (user_id,karaoke_id, title,artist,creator,tag, lyrics_lng,song_lng,Genre," \
                    "lyrics,is_deleted) VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"

            cursor.execute(query, (user_id, song_details.get("audio_id"), song_details.get("title"),
                                   song_details.get("artist"), song_details.get("creator"),
                                   json.dumps(song_details.get("tag")),song_details.get("lyrics_language"),
                                   song_details.get("song_language"), song_details.get("Genre"),
                                   json.dumps(song_details.get("lyrics")), 0))
            connection.commit()
            cursor.close()

            return "success","successfully uploaded"
        except Exception as e:
            return "Failed", "Something went wrong" + str(e)
        finally:
            if connection is not None:
                connection.close()
    def get_song_data(self,user_id):
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query = "Select * from songs where user_id=%(user_id)s"
            cursor.execute(query, {"user_id":user_id})
            data=cursor.fetchall()
            if data is not None and len(data)>0:
                connection.commit()
                cursor.close()
                return "success", "successfully uploaded",data
            else:
                return "Failed", "data not found in db",[]
        except Exception as e:
            return "Failed", "Something went wrong" + str(e),[]
        finally:
            if connection is not None:
                connection.close()
    
    def authorize_karaoke(self,id,table_name):
        connection = DbConnection.getDbConnection()
        cursor = connection.cursor()
        query_string = "select * from " + str(table_name) + " where karaoke_id =%(id)s AND is_authorized=0"
        cursor.execute(query_string, {"id": id})
        is_karaoke_exist=cursor.fetchall()
        if is_karaoke_exist is not None and len(is_karaoke_exist) > 0:
                authorize_query_string =  "UPDATE " + str(table_name) + " SET  is_authorized=1  WHERE karaoke_id =%(id)s "
                cursor.execute(authorize_query_string,{"id": id})
                cursor.close()
                connection.commit()
                return "success", "Karaoke authorized successfully"
        if len(is_karaoke_exist)==0:
            query_string = "select * from " + str(table_name) + " where karaoke_id =%(id)s AND is_authorized=1"
            cursor.execute(query_string, {"id": id})
            is_karaoke_authorized = cursor.fetchall()
            if is_karaoke_authorized is not None and len(is_karaoke_authorized) > 0:
                try:
                    unauthorize_query_string = "UPDATE " + str(table_name) + " SET  is_authorized=0  WHERE karaoke_id =%(id)s "
                    cursor.execute(unauthorize_query_string,{"id": id})
                    cursor.close()
                    connection.commit()
                    return "success", "karaoke unauthorized successfully"

                except Exception as e:
                    print(e)
                    return "Failed", "Something went wrong"

                finally:
                    if connection is not None:
                        connection.close()
        else:
            return "failed","Something went Fishy"


    def delete_karaoke(self,id,table_name1,table_name2):
        connection = DbConnection.getDbConnection()
        cursor = connection.cursor()
        query_string = "select * from " + str(table_name1) + " where ID =%(id)s AND is_deleted=0"
        cursor.execute(query_string, {"id": id})
        is_karaoke_exist=cursor.fetchall()
        if is_karaoke_exist is not None and len(is_karaoke_exist) > 0:
                query_string1 =  "UPDATE " + str(table_name1) + " SET  is_deleted=1  WHERE ID = %(id)s "
                cursor.execute(query_string1,{"id": id})
                query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=1  WHERE karaoke_id =%(id)s "
                cursor.execute(query_string2,{"id": id})
                cursor.close()
                connection.commit()
                return "success", "karaoke has been deleted successfully"
        if len(is_karaoke_exist)==0:
            query_string = "select * from " + str(table_name1) + " where ID =%(id)s AND is_deleted=1"
            cursor.execute(query_string, {"id": id})
            is_user_deleted = cursor.fetchall()
            if is_user_deleted is not None and len(is_user_deleted) > 0:
                try:
                    query_string1 =  "UPDATE " + str(table_name1) + " SET  is_deleted=0  WHERE ID = %(id)s "
                    cursor.execute(query_string1,{"id": id})
                    query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=0  WHERE karaoke_id =%(id)s "
                    cursor.execute(query_string2,{"id": id})
                    cursor.close()
                    connection.commit()
                    return "success", "karaoke has been undeleted successfully"

                except Exception as e:
                    print(e)
                    return "Failed", "Something went wrong"

                finally:
                    if connection is not None:
                        connection.close()
        else:
            return "failed","Something went Fishy"

    def update_song_data(self,song_details,user_id,id,tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where karaoke_id=%(id)s and is_deleted=0"
            cursor.execute(query_string,{"id":id})
            data = cursor.fetchall()
            if data is not None and len(data) > 0:
                query_update_string1="UPDATE " + str(tb_name) + " SET title = %(title)s ,artist=%(artist)s,creator=%(creator)s,tag=%(tag)s,lyrics_lng=%(lyrics_lng)s,song_lng=%(song_lng)s,Genre=%(Genre)s,updated_by=%(updated_by)s WHERE karaoke_id =%(id)s"
                cursor.execute(query_update_string1,{"title":song_details.get("title"),"artist":song_details.get("artist"),"creator":song_details.get("creator"),"tag": json.dumps(song_details.get("tag")),"lyrics_lng":song_details.get("lyrics_language"),"song_lng":song_details.get("song_language"),"Genre":song_details.get("Genre"),"updated_by":user_id,"id":id})
                connection.commit()
                cursor.close()
                return "success","successfully updated"
            else:
                return "Failed","Record not found"
        except Exception as e:
            return "Failed", "Something went wrong" + str(e)
        finally:
            if connection is not None:
                connection.close()