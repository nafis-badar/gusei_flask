from com.gusei.dbConnections.DbConnection import DbConnection
import json

class User:

    def insert_signup_data(self, fname, lname, email, password,social_type,social_id, phone_no, role,created_by, reg_date, update_date,
                           table_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()

            query_string = "select * from " + str(table_name) + " where user_email =%(email)s"
            cursor.execute(query_string,{"email":email})
            is_email_exists = cursor.fetchall()
            if is_email_exists is not None and len(is_email_exists) > 0:
                return "Failed", "Email Id already existed, Please try login"
            print("xyz")
            query_signup_string = "INSERT INTO " + str(
                table_name) + "(first_name, last_name, user_email, social_type,social_id, phone_no, role,created_by,registration_date,updated_date,is_deleted) VALUES (%s, %s, %s,%s, %s,%s, %s,%s,%s,%s,%s)"
            print(query_signup_string)
            cursor.execute(query_signup_string,(fname,lname,email,social_type,social_id,phone_no,role,created_by,reg_date,update_date,0))

            query_login_string = "INSERT INTO user_login (role,user_email, password,social_type,social_id, session_list,is_deleted) VALUES (%s, %s,%s, %s,%s,%s,%s)"
            cursor.execute(query_login_string,(role,email,password,social_type,social_id,"[]",0))
            cursor.close()
            connection.commit()
            return "success", "User has been added successfully"

        except Exception as e:
            print(e)
            return "Failed", "Something went wrong"
        finally:
            if connection is not None:
                connection.close()

    def findUserByEmail(self,email,tb_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()
            query_string = "select * from " + str(tb_name) + " where user_email = %(email)s"
            cursor.execute(query_string,{"email":email})
            is_email_exists = cursor.fetchall()
            if is_email_exists is not None and len(is_email_exists) > 0:
                return "success",is_email_exists[0]['password'],is_email_exists[0]['session_list']
            else:
                return "Failed", "Email id does not Exist",""
        except Exception as e:
            print(e)
            return "Failed", "Something went wrong",""
        finally:
            if connection is not None:
                connection.close()

    def insert_update_data(self, fname, lname, phone_no, user_id, update_date,
                           id,table_name):
        connection = None
        try:
            connection = DbConnection.getDbConnection()
            cursor = connection.cursor()

            # query_string = "select * from " + str(table_name) + " where ID =%(user_id)s AND is_deleted=0"
            # cursor.execute(query_string, {"user_id": user_id})
            # query_update_string = "INSERT INTO " + str(
            #     table_name) + "(first_name, last_name, phone_no, updated_date,is_deleted) VALUES ( %s,%s,%s,%s,%s)"

            # query_update_string = "UPDATE " + str(table_name) + " SET " + "(first_name, last_name, phone_no, updated_date)" \
            #     " VALUES ( %s,%s,%s,%s)" + " WHERE '" + str(table_name) + "'.'ID'=" + str(user_id)

            # query_update_string = "UPDATE " + str(table_name) + "SET "+"( first_name =% s, last_name =% s, phone_no =% s, updated_date =% s)" + " WHERE ID = "+str(user_id)

            query_update_string = "UPDATE " + table_name + " SET " + "first_name ='" + str(
                fname) + "',last_name='" + str(lname) + "',phone_no='" + str(phone_no) + "',updated_date='" + str(
                update_date) + "' WHERE ID = " + str(id)

            print(query_update_string)
            # cursor.execute(query_update_string,(fname,lname,phone_no,update_date))
            cursor.execute(query_update_string)
            cursor.close()
            connection.commit()
            return "success", "User has been updated successfully"

        except Exception as e:
            print(e)
            return "Failed", "Something went wrong"
        finally:
            if connection is not None:
                connection.close()

    def deleteUser(self,id,user_id,table_name1,table_name2):
        connection = DbConnection.getDbConnection()
        cursor = connection.cursor()
        query_string = "select * from " + str(table_name1) + " where ID =%(id)s AND is_deleted=0"
        cursor.execute(query_string, {"id": id})
        is_user_exist=cursor.fetchall()
        if is_user_exist is not None and len(is_user_exist) > 0:
                query_string1 =  "UPDATE " + str(table_name1) + " SET  is_deleted=1" + " ,deleted_by = "+str(user_id) + " WHERE ID = " + str(id)
                cursor.execute(query_string1)
                query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=1" + " WHERE ID = " + str(id)
                cursor.execute(query_string2)
                cursor.close()
                connection.commit()
                return "success", "User has been deleted successfully"
        if len(is_user_exist)==0:
            query_string = "select * from " + str(table_name1) + " where ID =%(id)s AND is_deleted=1"
            cursor.execute(query_string, {"id": id})
            is_user_deleted = cursor.fetchall()
            if is_user_deleted is not None and len(is_user_deleted) > 0:
                try:
                    query_string1 = "UPDATE " + str(table_name1) + " SET  is_deleted=0" + " ,deleted_by = 0"+ " WHERE ID = " + str(id)
                    cursor.execute(query_string1)
                    query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=0" + " WHERE ID = " + str(id)
                    cursor.execute(query_string2)
                    cursor.close()
                    connection.commit()
                    return "success", "User has been Undeleted successfully"

                except Exception as e:
                    print(e)
                    return "Failed", "Something went wrong"

                finally:
                    if connection is not None:
                        connection.close()
        else:
            return "failed","Something went Fishy"

    def blockUser(self, id, user_id, table_name):
        connection = DbConnection.getDbConnection()
        cursor = connection.cursor()
        query_string = "select * from " + str(table_name) + " where ID =%(id)s AND is_deleted=0 and is_blocked=0"
        cursor.execute(query_string, {"id": id})
        is_user_exist = cursor.fetchall()
        print(is_user_exist)
        if is_user_exist is not None and len(is_user_exist) > 0:
            query_string1 = "UPDATE " + str(table_name) + " SET  is_blocked=1" + " ,blocked_by = " + str(
                user_id) + " WHERE ID = " + str(id)
            cursor.execute(query_string1)
            # query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=1" + " WHERE ID = " + str(id)
            # cursor.execute(query_string2)
            cursor.close()
            connection.commit()
            return "success", "User has been blocked successfully"

        if len(is_user_exist) == 0:
            query_string = "select * from " + str(table_name) + " where ID =%(id)s AND is_blocked=1"
            cursor.execute(query_string, {"id": id})
            is_user_blocked = cursor.fetchall()
            if is_user_blocked is not None and len(is_user_blocked) > 0:
                try:
                    query_string1 = "UPDATE " + str(
                        table_name) + " SET  is_blocked=0" + " ,blocked_by = 0" + " WHERE ID = " + str(id)
                    cursor.execute(query_string1)
                    # query_string2 = "UPDATE " + str(table_name2) + " SET  is_deleted=0" + " WHERE ID = " + str(id)
                    # cursor.execute(query_string2)
                    cursor.close()
                    connection.commit()
                    return "success", "User has been Unblocked successfully"

                except Exception as e:
                    print(e)
                    return "Failed", "Something went wrong"

                finally:
                    if connection is not None:
                        connection.close()
        else:
            return "failed", "Something went Fishy"


