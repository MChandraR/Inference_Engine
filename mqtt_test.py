
import math
import json
import time
import paho.mqtt.client as mqtt
from threading import Thread,Timer
import asyncio
from utils.folder import save_to_excel

class myMqtt:
    def __init__(self, socket) -> None:
        self.data = []
        self.counter = 1
        self.lintasan = 'B'
        self.lats = [
                0.868404,
                0.868457667,
                0.868474667,
                0.868554333,
                0.868582,
                0.868603833,
                0.868637833,
                0.868687333,
                0.8686555,
                0.868617333,
                0.868567,
                0.868578,
                0.868485167,
                0.868523,
                0.868493,
                0.868466167,
                0.868396833,
                0.868327
            ]
        
        self.Lons = []
        self.Lats = []
        self.captureCounter = 11
        self.inverseCounter = 8
        self.stopPoints = [16]
        self.stopPoint = self.stopPoints

        self.lons = [
            104.4595808,
            104.4595997,
            104.4596475,
            104.4596248,
            104.4595923,
            104.4595682,
            104.4595358,
            104.459537,
            104.4594853,
            104.4594268,
            104.4593945,
            104.4593102,
            104.4592867,
            104.4593352,
            104.4594312,
            104.4593508,
            104.4595442,
            104.4594927
        ]
        
        self.inversed = False
        self.inv = 0 if self.lintasan == 'B' else 1
        
        self.form = None
        self.speed = 1650
        self.speedKm = 0

        self.Kp = 1.0
        self.Ki = 0.0
        self.Kd = 0.1
        self.radius = 0.8
        self.lat = 0
        self.lon = 0
        self.azm = 0
        self.speed = 1650
        self.latDir = 0
        self.lonDir = 0
        self.sog = 0
        self.cog = 0
        self.azimuth = 0

        self.setpoint = 0
        self.motor = 0
        self.inputs = 0
        self.output = 0
        self.integral = 0
        self.previous_error = 0
        self.previous_time = 0
        self.mqttc = socket
        self.mqttc.on("data", self.on_message)
        self.sendPub()
        #self.sendData()
        
    def loadConf(self):
        with open("conf.json", "r") as data:
            conf = json.load(data)
            self.Kp = float(conf["kp"])
            self.Ki = float(conf["ki"])
            self.Kd = float(conf["kd"])
        
    def getPosition(self):
        if self.counter < self.captureCounter:
            return "FLOATING BALL"
        else: return "CAPTURE BOX"
    
    def getProgress(self):
        if self.counter < self.captureCounter:
            return self.counter/self.captureCounter* 100;
        else: return abs(self.counter-self.captureCounter)/abs(self.captureCounter-len(self.lats)) * 100;

    def reset(self):
        self.stopPoint = self.stopPoints
        self.inversed = False

    def turnOnMotor(self):
        self.motor = 1

    def sendPub(self):
        self.mqttc.emit("setLats", {
            "event" : "setLats",
            "lats" : self.lats
        })
        self.mqttc.emit("setLongs",{
            "event" : "setLongs",
            "longs" : self.lons
        })
        
    def sendData(self):
        while True:
            time.sleep(.4)
            res = {
                "event" : "conf",
                "kp" : self.Kp,
                "radius" : self.radius,
                "kd" : self.Kd,
                "ki" : self.Ki,
		        #"counter":self.counter,
                "motor" : self.motor,
                "speed" : self.speed if self.counter < len(self.lats) else 1550
            }
           
            if self.counter in self.stopPoint and self.motor == 1:
                self.stopPoint.remove(self.counter)
                self.motor = 0
                tim = Timer(5, self.turnOnMotor, None)
                tim.start()
                
            if self.form is not None: self.form.log_res.set(str(res))
            self.mqttc.emit("conf", res)

    def on_message(self,data):
        print("Dapat data cuy")
        self.lat = data['lat']
        self.lon = data['lon']
        self.azimuth = data['adjAzimut']
        self.latDir = data['latDirection']
        self.lonDir = data['lonDirection']
        self.sog = data['speed']
        self.cog = data['adjHeading']
        # self.speedKm = data["speedKm"]
        self.counter = data["counter"]
        
       
        
        if self.counter >= self.inverseCounter and not self.inversed:
            self.inv  = not self.inv
            self.inversed = True

        if self.form is not None:
            self.form.log_value.set(  ("\n" + str(data)[0:200]))
            self.form.lat_value.set(self.lat)
            self.form.counter_value.set(str(data["counter"]))
            self.form.coordinate_value.set(self.azimuth)
            self.form.long_value.set(self.lon)
            self.form.ld_value.set(data['latDirection'])
            self.form.lgd_value.set(data['lonDirection'])
            self.form.lat2_value.set(str(self.lats[self.counter-1]))
            self.form.lon2_value.set(str(self.lons[self.counter-1]))
            self.form.lat1Value.set(str(self.lats[0]))
            self.form.lat2Value.set(str(self.lats[1]))
            self.form.lat3Value.set(str(self.lats[2]))
            self.form.lat4Value.set(str(self.lats[3]))
            self.form.lat5Value.set(str(self.lats[4]))
            self.form.lat6Value.set(str(self.lats[5]))
            
        # self.data.extend(["wakti","0",self.cog,self.sog,"Sun", "23",self.latDir, self.lat, self.lonDir,self.lon])
        # save_to_excel(self.data)
  

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setForm(self, form):
        self.form = form


thread = None
mymqtt = None
def mqtt(socket):
    global thread, mymqtt
    mymqtt = myMqtt(socket)






