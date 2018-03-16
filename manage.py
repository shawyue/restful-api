# _*_coding:utf-8 _*_
from flask_script import Manager
from app import create_app

app = create_app("testing")
manager = Manager(app)

@manager.option('-u', '--username', help='Your name')
@manager.option('-p', '--password', help='Your password')
def admin(username, password):
    "create administrator"
    from app.models import RegisterUser
    
    re = RegisterUser.register_admin(username, password)
    print(re)

if __name__ == '__main__':
    manager.run()