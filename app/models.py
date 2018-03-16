# _*_ coding:utf-8 _*_
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for, g
import datetime
import re
from logbook import Logger


from . import mysql_client

log = Logger("MODELS")



class GenerateArticleID(object):

    def __new__(cls):
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(GenerateArticleID, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.get_max_id()


    def get(self):
        if self.max_article_id == None:
            self.max_article_id = 1000
            return self.max_article_id
        else:
            self.max_article_id = self.max_article_id + 1
            return self.max_article_id

    def get_max_id(self):
        self.max_article_id = mysql_client.fetch_one("SELECT MAX(ID) FROM ARTICLES")[0]
        return self.max_article_id

class ApiPermission(object):
    def __init__(self, article_id):
        self._artice_id = article_id
    
    def read_permission(self):
        return True

    def update_permission(self):
        if g.user.is_self_article(self._artice_id):
            return True
        return False

    def delete_permission(self):
        if(g.user.is_adminstrator()):
            return True
        elif(g.user.is_self_article(self._artice_id)):
            return True
        else:
            return False


class ApiArticle(object):
    def __init__(self):
        self.article_id_obj = GenerateArticleID()
        self.user_id = g.user.get_id()

    def create_article(self, content):
        now_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            article_id = self.article_id_obj.get()
            mysql_client.execute("INSERT INTO ARTICLES VALUES(%s, %s, %s, %s, %s)", (article_id,self.user_id, content, now_time, now_time))
            mysql_client.commit()
        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        return {
            "id": article_id, 
            "content":content,
            "link":{
            "self": url_for('api.get_article', article_id=article_id), 
            "update":url_for('api.update_article', article_id=article_id), 
            "delete":url_for('api.delete_article', article_id=article_id)
            }
        }

    def update_article(self, article_id, content):
        permission = ApiPermission(article_id)
        if permission.update_permission() == False:
            return {"status": -1, "msg":"Permission denied"}
            
        now_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            mysql_client.execute("UPDATE ARTICLES SET CONTENT=%s, MODIFYTIME=%s WHERE ID=%s", (content, now_time, article_id))
            mysql_client.commit()
        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        return {
            "id": article_id, 
            "new_content":content, 
            "link":{
                "self": url_for('api.get_article', article_id=article_id), 
                "update":url_for('api.update_article', article_id=article_id), 
                "delete":url_for('api.delete_article', article_id=article_id)
                }
            }

    def get_article(self, article_id = None):
        permission = ApiPermission(article_id)
        if permission.read_permission() == False:
            return {"status": -1, "msg":"Permission denied"}
        try:
            if(article_id):
                content = mysql_client.fetch_one("SELECT CONTENT FROM ARTICLES WHERE ID=%s", (article_id))
                return {"data":content[0]}

            else:
                content_list = mysql_client.fetch_all("SELECT ID, CONTENT FROM ARTICLES")
                data = {}
                for article_id, content in content_list:
                    data["url"] = url_for("api.get_article", article_id=article_id)
                    data["content"] = content
                return {"data":data}

        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        
    def delete_article(self, article_id):
        permission = ApiPermission(article_id)
        if permission.delete_permission() == False:
            return {"status": -1, "msg":"Permission denied"}
        try:
            mysql_client.execute("DELETE FROM ARTICLES WHERE ID=%s", (article_id))
            mysql_client.commit()
        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        return {
                "msg":"deleted successfully", 
                "link":{"all": url_for('api.get_all_article')}
            }    

class User(object):

    def __init__(self, user_id):
        
        #self.username = username
        self.id = user_id
        self.password_hash = self.get_password_hash()

    @property
    def role(self):
        user_type = mysql_client.fetch_one("SELECT R.NAME FROM USERS U LEFT JOIN ROLE R ON U.ROLEID = R.ID WHERE U.ID=%s", (self.id))
        if user_type != None:
            return user_type[0]
        return None

    @property
    def username(self):
        return mysql_client.fetch_one("SELECT NICKNAME FROM USERS WHERE ID=%s", (self.id))[0]

    @property
    def password(self):
        raise AttributeError("password is not readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        mysql_client.execute("UPDATE USERS SET PASSWD = %s WHERE ID = %s",(self.password_hash, self.id))
        mysql_client.commit()

    def verify_password(self, password):
        res = check_password_hash(self.password_hash, password)
        log.debug(res)
        return res
    def get_password_hash(self):
        user_info = mysql_client.fetch_one("SELECT PASSWD FROM USERS WHERE ID = %s", (self.id))
        if user_info is not  None:
            return user_info[0]
    
    @staticmethod
    def generate_token(json_data, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(json_data)
    
    @staticmethod
    def parse_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        return data

    def get_id(self):
        return str(self.id)

    def is_adminstrator(self):
        user_type = self.role
        log.debug(user_type)
        if user_type == "ADMINISTRATOR":
            return True
        else:
            return False

    def is_self_article(self, article_id):
        user_id = mysql_client.fetch_one("SELECT USERID FROM ARTICLES WHERE ID=%s", (article_id))[0]
        if(int(self.id) == int(user_id)):
            return True
        else:
            return False


class RegisterUser(object):

    def __init__(self):
        pass
    
    @staticmethod
    def register_admin(username, password):
        if (username != None and password != None):
            admin_id = mysql_client.fetch_one("SELECT ID FROM ROLE WHERE NAME = %s", "ADMINISTRATOR")[0]
            password_hash = generate_password_hash(password)
            mysql_client.execute("INSERT INTO USERS (id, nickname, passwd, roleid) VALUES(0, %s, %s, %s)", (username, password_hash, admin_id))
            mysql_client.commit()
            user_id = RegisterUser.get_id(username)
            return {"username":username, "msg":"Registered Successfully" }
        return {"username":username, "msg":"Registration failed"}

    @staticmethod
    def get_id(username):
        if username is not None:
            id_info = mysql_client.fetch_one("SELECT ID FROM USERS WHERE nickname = %s", (username))
            log.debug(id_info)
            if id_info is not None:
                return id_info[0]
            else:
                return None

    @staticmethod   
    def verify_username(username):
        #log.debug(username)
        id_info = mysql_client.fetch_one("SELECT ID FROM USERS WHERE nickname = %s", (username))
        log.debug(id_info)
        if id_info is None:
            return True
        else:
            return False

    @staticmethod
    def register( user_info):
        
        username = user_info.get("username", None)
        password = user_info.get("password", None)
        if (username != None and password != None):
            password_hash = generate_password_hash(password)
            normal_id = mysql_client.fetch_one("SELECT ID FROM ROLE WHERE NAME = %s", "NORMAL")[0]
            mysql_client.execute("INSERT INTO USERS (id, nickname, passwd, roleid) VALUES(0, %s, %s, %s)", (username, password_hash, normal_id))
            mysql_client.commit()
            user_id = RegisterUser.get_id(username)
            return True
        return False