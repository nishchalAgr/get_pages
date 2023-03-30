from getpages import get_pages as gp
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import atexit
import os

app = Flask(__name__)

load_dotenv(find_dotenv())

client = MongoClient(os.getenv('MongoURL'))
db = client.pages

doc_id = -1

count = 0

def refresh():
    global doc_id
    arr = gp(os.getenv('Github_Username'), os.getenv('APIKey'))

    if db.pages.find_one() is None:
        doc_id = db.pages.insert_one({"pages":arr}).inserted_id
        return
    
    if doc_id == -1:
        doc_id = db.pages.find_one()["_id"]
    db.pages.update_one({"_id":doc_id}, {"$set":{"pages":arr}})    

@app.route("/pages")
def getpages():
    global doc_id
    arr = db.pages.find_one({"_id":doc_id})['pages']
    return {"pages":arr}

refresh()

scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh, trigger="interval", seconds=60*60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
