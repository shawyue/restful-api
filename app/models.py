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






def is_adminstrator(id):
    if(id == 1):
        return True

def is_self_article(uid, article_id):
    user_id = mysql_client.fetch_one("SELECT USERID FROM ARTICLES WHERE ID=%s", (article_id))[0]
    if(int(uid) == int(user_id)):
        return True
    else:
        return False

class ApiArticle(object):
    def __init__(self):
        self.article_id_obj = GenerateArticleID()
        self.user_id = g.current_user

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
        try:
            if(article_id):
                content = mysql_client.fetch_one("SELECT CONTENT FROM ARTICLES WHERE ID=%s", (article_id))
                return {"data":content[0]}

            else:
                content_list = mysql_client.fetch_all("SELECT CONTENT FROM ARTICLES")
                data = []
                for line in content_list:
                    data.append(line[0])
                return {"data":data}

        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        
    def delete_article(self, artice_id):
        try:
            mysql_client.execute("DELETE FROM ARTICLES WHERE ID=%s", (artice_id))
            mysql_client.commit()
        except Exception as e:
            msg = str(e)
            log.error(msg)
            return {"status":-1, "error":msg}
        return {
                "msg":"deleted successfully", 
                "link":{"all": url_for('api.get_all_article')}
            }    


class ApiPermission(object):
    def __init__(self, uid, article_id):
        self._user_id = uid
        self._artice_id = article_id
    
    def read_permission(self):
        return True

    def write_permission(self):
        if(is_adminstrator(self._user_id)):
            return True
        elif(is_self_article(self._user_id, self._artice_id)):
            return True
        else:
            return False



class User(object):

    def __init__(self, user_id):
        
        #self.username = username
        self.id = user_id
        self.password_hash = self.get_password_hash()

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

    @staticmethod
    def get(user_id):
        if user_id is not None:
            return User(user_id)
        else:
            return None


class RegisterUser(object):

    def __init__(self):
        pass
    
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
        log.debug(username)
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
            mysql_client.execute("INSERT INTO USERS (id, nickname, passwd, roleid) VALUES(0, %s, %s, 2)", (username, password_hash))
            mysql_client.commit()
            user_id = RegisterUser.get_id(username)
            return True
        return False

    
