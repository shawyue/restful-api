# 用户权限验证系统

注意：Python使用的为Python3, MySQL应该使用utf-8字符集

## 构建windows环境

1、请确保已经安装了Python3和virtualenv

2、使用virtualenv创建独立运行环境

        virtualenv --no-site-packages venv 注意华景变量配置的Python

3、安装依赖包

        .\venv\Scripts\activate 启动独立运行环境
        pip install -r requirements.txt 安装依赖包

4、安装mysql数据库(已安装或者有远程可用mysql数据的跳过)

5、使用database.sql中sql创建初始化数据库

6、修改 config.py 中的数据配置

7、在命令行中创建管理员账户

        manage.py admin -u USERNAME -p PASSWORD 创建管理员账户

8、启动

        manage.py runserver --host 0.0.0.0 --port 端口号

9、创建普通用户

        使用 POST http://127.0.0.1:5000/api/v1.0/users 即可创建

10、测试用户权限验证系统

## 构建Linux环境

1、请确保已经安装了Python3和virtualenv

2、使用virtualenv创建独立运行环境

    virtualenv --no-site-packages --python=python3 venv
    
3、安装依赖包

        source ./venv/bin/activate 启动独立运行环境
        pip3 install -r requirements.txt 安装依赖包

4、安装mysql数据库(已安装或者有远程可用mysql数据的跳过)

        sudo apt-get install redis-server
        sudo apt-get install mysql-server
        sudo apt-get install mysql-client

5、使用database.sql中sql创建初始化数据库

6、修改 config.py 中的数据配置

7、在命令行中创建管理员账户

        manage.py admin -u USERNAME -p PASSWORD 创建管理员账户

8、启动

        Python3 manage.py runserver --host 0.0.0.0 --port 端口号

9、创建普通用户

        使用 POST http://127.0.0.1:5000/api/v1.0/users 即可创建

10、测试用户权限验证系统

## URL说明

    POST http://127.0.0.1:5000/api/v1.0/users                 #创建用户(为普通用户)
    GET http://127.0.0.1:5000/api/v1.0/users                  #获取当前用户信息

    GET http://127.0.0.1:5000/api/v1.0/article                #获得所有文章
    GET http://127.0.0.1:5000/api/v1.0/article/article_id     #获得指定文章
    POST http://127.0.0.1:5000/api/v1.0/article               #创建一篇文章(content放文本内容)
    put http://127.0.0.1:5000/api/v1.0/article/article_id     #更新指定文章(content放文本内容)
    DELETE http://127.0.0.1:5000/api/v1.0/article/article_id  #删除指定文章
