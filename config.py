# _*_ coding:utf-8 _*_

class Config:
    
    SECRET_KEY = "123456"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 #限制上传文件大小100M

    LOGBOOK_CONSOLE_LEVEL = 'DEBUG'   #'DEBUG','INFO','NOTICE','WARNING','ERROR','CRITICAL'
    LOGBOOK_FILE_LEVEL = 'NOTICE'  #'DEBUG','INFO','NOTICE','WARNING','ERROR','CRITICAL'
    LOGBOOK_LOG_FILE = 'logs/log.log'
    LOGBOOK_BACKUP_COUNT = 5
    LOGBOOK_MAX_SIZE = 1024
    LOGBOOK_FORMAT_STRING ='({record.time:%Y-%m-%d %H:%M:%S}),{record.level_name},[{record.thread_name}],{record.channel}[{record.lineno}]: {record.message}'
    #simple version: format_string = '({record.time:%m-%d %H:%M:%S}){record.level_name},channel:{record.channel},line_{record.lineno}: {record.message}'

class TestingConfig(Config):
    DEBUG = True
   
    MYSQL_HOST = "192.168.190.150"
    MYSQL_PORT = 3306
    MYSQL_USER = "restful"
    MYSQL_PASSWORD = "restful"
    MYSQL_DB = "api"
    MYSQL_CHARSET = "utf8"

    LOGBOOK_CONSOLE = True
    LOGBOOK_FILE = True


config = {
    'testing': TestingConfig,
    'default': TestingConfig
}