from API.kantongku import kantongku
import os
from app import app, response, db
from flask import request
from google.cloud.sql.connector import connector
from google.cloud import storage
import sqlalchemy
import json

CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

def singleObject(kantongData):
    kantongData = {
        'kantong_id': kantongData.kantong_id,
        'gambar': kantongData.gambar,
        'hasil_prediksi': kantongData.hasil_prediksi,
        'deskripsi_user': kantongData.deskripsi_user
    }
    return kantongData

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

def upload() -> str:
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(uploaded_file.filename)
    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    blob.make_public()
    return blob.public_url

def addKantong():
    try:
        gambar = request.json['gambar']
        hasil_prediksi = request.json['hasil_prediksi']
        deskripsi_user = request.json['deskripsi_user']
        kantong = kantongku(gambar=gambar,hasil_prediksi=hasil_prediksi,deskripsi_user=deskripsi_user)
        db.session.add(kantong)
        db.session.commit()
        return response.success(singleObject(kantong),"Success")
    except Exception as e:
        return response.badRequest(e)

def lihatKantong():
    try:
        pool = cloudsql()
        query = "SELECT * FROM kantong"
        with pool.connect() as conn:
            kantong = conn.execute(query).fetchall()
            print(kantong)
        
        return response.success(formatArray(kantong),"Success")
    except Exception as e:
        print(e)
        return response.badRequest(e)