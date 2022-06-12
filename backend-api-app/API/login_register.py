import json
import sqlalchemy
from API.userId import userId
from app import app, response, db
from flask import request
from google.cloud.sql.connector import connector

def singleObject(dataUser):
    dataUser = {
        'user_id': dataUser.user_id,
        'full_name': dataUser.full_name,
        'email': dataUser.email,
        'password': dataUser.password
    }
    return dataUser

def formatArray(data):
    arr = []

    for d in data:
        arr.append(singleObject(d))

    return arr

def cloudsql() -> sqlalchemy.engine.Engine:
    def getconn() -> connector.connect:
        conn = connector.connect(
            "project-capstone-c22-ps348:asia-southeast2:db-cpstn-c22-ps348",
            "pymysql",
            user="root",
            password="12345678910",
            db="db-project"
        ) 
        return conn

    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return engine

def showUser():
    try:
        pool = cloudsql()
        query = "SELECT * FROM user"
        with pool.connect() as conn:
            user = conn.execute(query).fetchall()
            print(user)

        return response.success(formatArray(user),"Success")

    except Exception as e:
        print(e)
        return response.badRequest(e)

def login():
    data = json.loads(request.data)
    try:
        email = data['email']
        password = data['password']

        pool = cloudsql()
        query = "SELECT * FROM user where email = '"+email+"' and password = '"+password+"'"
        with pool.connect() as conn:
            user = conn.execute(query).fetchall()
            print(user)

        if user is None:
            return response.badRequest("Email or Password wrong")
        return response.success(singleObject(user),"Success")
    
    except Exception as e:
        return response.badRequest(e)

def register():
    try:
        full_name = request.json['full_name']
        email = request.json['email']
        password = request.json['password']
        user = userId(full_name=full_name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return response.success(singleObject(user),"Success")
    
    except Exception as e:
        return response.badRequest(e)