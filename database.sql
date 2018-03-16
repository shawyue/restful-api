
create database api; --创建数据库

create user 'username'@'host' identified by 'password'; --创建mysql用户,host设为%可在任意主机登录
GRANT all privileges ON api.* TO 'username'@'host'; --赋予用户权限 

create table ROLE(
    id int unsigned,
    name varchar(50) unique not null,
    primary key(id)
);
--插入基础数据
insert into ROLE values(1,'ADMINISTRATOR'); --admin
insert into ROLE values(2,'NORMAL');      --用户

-- 创建用户表
create table USERS (
    id int unsigned auto_increment,
    nickname varchar(50) not null ,
    passwd char(128) not null,
    roleID int unsigned not null, 
    signUpDate datetime,
    unique(nickname),
    primary key(id)
);

--创建文章表
create table ARTICLES(
    id int unsigned auto_increment,
    userID int unsigned not null,
    content mediumtext,
    createTime datetime,
    modifyTime datetime,
    primary key(id)
);
