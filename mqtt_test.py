
import math
import json
import paho.mqtt.client as mqtt
import threading
import asyncio

class myMqtt:
    def __init__(self) -> None:
        self.counter = 1
        self.lats = [
            0.868491167,
            0.868552667,
            0.868569833,
            0.868505333,
            0.868465833,
            0.868416833,
            0.868409333,
            0.868484333
        ]

        self.lons = [
            104.4592822,
            104.459324,
            104.459437,
            104.4594323,
            104.4594418,
            104.4595032,
            104.4594673,
            104.4592832
        ]
        
        self.form = None
        self.speed = 1650
        self.speedKm = 0

        self.Kp = 1.0
        self.Ki = 0.0
        self.Kd = 0.1
        self.inv = 0
        self.radius = 1
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
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe# Use current time for initialization

    def calculate_heading(self, lat1, lon1, lat2, lon2):
        delta_lon = lon2 - lon1
        x = math.cos(math.radians(lat2)) * math.sin(math.radians(delta_lon))
        y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
            math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon))
        
        heading = math.atan2(x, y) * 180.0 / math.pi

        if heading < 0:
            heading += 360.0
        
        return heading

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000.0  # Radius of Earth in meters

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)

        a = math.sin(dLat / 2.0) * math.sin(dLat / 2.0) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dLon / 2.0) * math.sin(dLon / 2.0)

        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        return R * c

    def on_connect(self, mqttc, obj, reason_code, properties):
        mqttc.subscribe("sensor/data", 0)
        self.sendPub()
        print("Connected to %s:%s" % (mqttc._host, mqttc._port))
    
    def sendPub(self):
        self.mqttc.publish("data/setLats", json.dumps({
            "lats" : self.lats
        }))
        self.mqttc.publish("data/setLongs", json.dumps({
            "longs" : self.lons
        }))

    def on_message(self, mqttc, obj, msg):
        data = json.loads(msg.payload.decode())
        print(data)

        self.lat = data['lat']
        self.lon = data['lon']
        self.azimuth = data['adjAzimut']
        self.latDir = data['latDirection']
        self.lonDir = data['lonDirection']
        self.sog = data['speed']
        self.cog = data['adjHeading']
        # self.speedKm = data["speedKm"]
        self.counter = data["counter"]

        if self.form is not None:
            self.form.log_value.set(  ("\n" + str(data)))
            self.form.lat_value.set(self.lat)
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
            
    
        
        res =  json.dumps({
            "kp" : self.Kp,
            "radius" : 0.8,
            "kd" : self.Kd,
            "ki" : self.Ki,
            "motor" : self.motor,
            "speed" : self.speed if self.counter < len(self.lats) else 1550
        })
        if self.form is not None: self.form.log_res.set(str(res))
        self.mqttc.publish("data/result", res)
  
            

    def on_subscribe(self, mqttc, obj, mid, reason_code_list):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))
       

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setForm(self, form):
        self.form = form


mymqtt = myMqtt()
thread = None
async def mqtt():
    global thread
    mqttc = mymqtt.mqttc
    mqttc.connect_async("192.168.1.105", 1883)
    mqttc.subscribe("sensor/data", 0)
    thread = threading.Thread(target=mqttc.loop_forever)
    thread.start()


asyncio.run(mqtt())



