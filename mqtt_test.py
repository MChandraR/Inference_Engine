
import math
import json
import time
import paho.mqtt.client as mqtt
from threading import Thread,Timer
import asyncio

class myMqtt:
    def __init__(self, socket) -> None:
        self.counter = 1
        self.lintasan = 'A'
        self.lats = [
                0.8683295,
                0.868379,
                0.868402167,
                0.8685135,
                0.868537,
                0.868569167,
                0.8685895,
                0.8686295,
                0.868592667,
                0.868561167,
                0.868511167,
                0.868513667,
                0.8684175,
                0.868448667,
                0.868442167,
                0.868405333,
                0.8682995,
                0.868227333
            ]
        
        self.Lons = []
        self.Lats = []
        self.captureCounter = 11
        self.inverseCounter = 8
        self.stopPoints = [16]
        self.stopPoint = self.stopPoints

        self.lons = [
            104.459583,
            104.4596005,
            104.459661,
            104.459643,
            104.4596063,
            104.4595873,
            104.4595565,
            104.4595333,
            104.4594858,
            104.45945,
            104.4594135,
            104.4593162,
            104.4593017,
            104.4593583,
            104.459415,
            104.4593538,
            104.4595668,
            104.4594733
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
        
    def getPosition(self):
        if self.counter < self.captureCounter:
            return "FLOATING BALL"
        else: return "CAPTURE BOX"
    
    def getProgress(self):
        if self.counter < self.captureCounter:
            return self.counter/self.captureCounter* 100;
        else: return abs(self.captureCounter-len(self.lats))/abs(self.counter-self.captureCounter) * 100;

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
            
        
  

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setForm(self, form):
        self.form = form


thread = None
mymqtt = None
def mqtt(socket):
    global thread, mymqtt
    mymqtt = myMqtt(socket)






