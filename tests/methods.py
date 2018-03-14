# _*_ coding:utf-8 _*_

import urllib.request

def get_data(url, data=None):
    req = urllib.request.Request(url, data=None, method="GET")
    res = urllib.request.urlopen(req)
    print(res.read())

def post_data(url, data):
    req = urllib.request.Request(url=url, data=data, method="POST")
    res = urllib.request.urlopen(req)
    print(res.read())

def put_data(url, data):
    req = urllib.request.Request(url=url, data=data, method="PUT")
    res = urllib.request.urlopen(req)
    print(res.read())

def delete_data(url):
    req = urllib.request.Request(url=url, method="DELETE")
    res = urllib.request.urlopen(req)
    print(res.read())

if __name__ == "__main__":

    #post_data("http://127.0.0.1:5000/api/v1.0/users", data=b"username=python&password=python")
    get_data("http://127.0.0.1:5000/api/v1.0/resource", data=b"username=python&password=python")
    """
    post_data("http://127.0.0.1:5000/api/v1.0/article", data = b"content=11111")
    get_data("http://127.0.0.1:5000/api/v1.0/article")
    get_data("http://127.0.0.1:5000/api/v1.0/article/1")
    put_data("http://127.0.0.1:5000/api/v1.0/article/1", data=b"content=33333")
    get_data("http://127.0.0.1:5000/api/v1.0/article")
    delete_data("http://127.0.0.1:5000/api/v1.0/article/5")
"""