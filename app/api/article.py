# _*_ coding:utf-8 _*_

from app.api import api
from app.models import ApiArticle, RegisterUser, User
from flask import g, jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth
from logbook import Logger

auth = HTTPBasicAuth()

log = Logger("API.ARTICLE")

@auth.verify_password
def verify_password(username, password):
    log.debug({"username":username, "password":password})
    if RegisterUser.verify_username(username) == False:
        user = User(RegisterUser.get_id(username))
        if user.verify_password(password):
            g.user = user
            return True
    return False
    
@api.route("/v1.0/users", methods=["GET"])
@auth.login_required
def get_user():
    return jsonify({
            "id":g.user.get_id(), 
            "username": g.user.username, 
            "role": g.user.role,
            "link":{
                "self": url_for('api.get_user'), 
                "sign_up": url_for('api.register_user'),
                "create_article": url_for("api.create_article"),
                "get_all_article": url_for("api.get_all_article")
            }
        })

@api.route("/v1.0/users", methods=["POST"])
def register_user():
    username = request.values.get("username", None)
    password = request.values.get("password", None)
    #log.debug(username)
    if username is None or password is None:
        return jsonify({"status":-3, "msg":"username or password error"}), 400
    if RegisterUser.verify_username(username) == False:
        return jsonify({"status":-3, "msg":"username already exists"})
    user_info = {"username":username, "password":password}
    log.debug(user_info)
    if RegisterUser.register(user_info):
        user = User(RegisterUser.get_id(username))
        return jsonify({"username":username, "msg":"Registered Successfully", "status": 0})
    return jsonify({"username":username, "msg":"Registration failed", "status":-2 })

@api.route("/v1.0/article", methods=["GET"])
@auth.login_required
def get_all_article():
    g.current_user = 1
    article_obj = ApiArticle()
    data = article_obj.get_article()
    return jsonify(data)


@api.route("/v1.0/article/<int:article_id>", methods=["GET"])
@auth.login_required
def get_article(article_id):
    g.current_user = 1
    article_obj = ApiArticle()
    data = article_obj.get_article(article_id)
    return jsonify(data)

@api.route("/v1.0/article", methods=["POST"])
@auth.login_required
def create_article():
    g.current_user = 1
    content = request.values.get("content", None)
    if(content):
        article_obj = ApiArticle()
        data = article_obj.create_article(content)
        return jsonify(data)
    else:
        return jsonify({"error":"no data"})
    

@api.route("/v1.0/article/<int:article_id>", methods=["PUT"])
@auth.login_required
def update_article(article_id):
    g.current_user = 1
    content = request.values.get("content", None)
    if(content):
        article_obj = ApiArticle()
        data = article_obj.update_article(article_id, content)
        return jsonify(data)
    else:
        return jsonify({"error":"no data"})

@api.route("/v1.0/article/<int:article_id>", methods=["DELETE"])
@auth.login_required
def delete_article(article_id):
    g.current_user = 1
    article_obj = ApiArticle()
    data = article_obj.delete_article(article_id)
    return jsonify(data)
