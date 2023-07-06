import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger
import random
import datetime
from flask import Flask, send_from_directory, request

s = BackgroundScheduler()

def getRandom():
    return random.randrange(1,10)
def test():
    print(getRandom())
    ct = datetime.datetime.now()
    print("current time:-", ct)

startHours = 20
endHours = 20


myTrigger = AndTrigger([IntervalTrigger(seconds=10),CronTrigger(hour=21)])


job = s.add_job(test, trigger=myTrigger, id='test_job')

s.start()

app = Flask(__name__, static_folder='../gardenfront/dist')
# Serve React App
@app.route('/')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route('/testendminutes', methods=['POST'])
def handle_json():
    data = request.json
    endMinutes = data.get('endMinutes')
    newTrigger = CronTrigger(hour='*', minute=f'{10}-{endMinutes}',second='*',jitter='3')
    print(endMinutes)
    s.reschedule_job('test_job',trigger=newTrigger)
    return data