# _*_ coding:utf-8 _*_

import urllib.request


headers = {
"Authorization":"Basic cHl0aG9uOnB5dGhvbg==",

"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

def get_data(url, data=None):
    req = urllib.request.Request(url, headers=headers, data=None, method="GET")
    res = urllib.request.urlopen(req)
    print(res.read())

def post_data(url, data):
    req = urllib.request.Request(url=url,headers=headers, data=data, method="POST")
    res = urllib.request.urlopen(req)
    print(res.read())

def put_data(url, data):
    req = urllib.request.Request(url=url, headers=headers, data=data, method="PUT")
    res = urllib.request.urlopen(req)
    print(res.read())

def delete_data(url, data):
    req = urllib.request.Request(url=url, headers=headers, data=data ,method="DELETE")
    res = urllib.request.urlopen(req)
    print(res.read())

if __name__ == "__main__":
    delete_data("http://127.0.0.1:5000/api/v1.0/article/6", data=b'username=root&password=admin')