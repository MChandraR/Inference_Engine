
import math
import json
import paho.mqtt.client as mqtt
import threading
import asyncio

class myMqtt:
    def __init__(self) -> None:
        self.counter = 1
        self.lats = [
            0.868477,
            0.868484833,
            0.868566667,
            0.868559,
            0.868510833,
            0.86844,
            0.868386167,
            0.868477
        ]

        self.lons = [
            104.459256,
            104.4592995,
            104.4594025,
            104.4594482,
            104.4594603,
            104.459547,
            104.4595215,
            104.459256,
        ]
        
        self.form = None
        self.speed = 1650

        self.Kp = 1.0
        self.Ki = 0.0
        self.Kd = 0.1
        self.inv = 0
        self.radius = 1

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
        print("Connected to %s:%s" % (mqttc._host, mqttc._port))
        mqttc.publish("data/setPoints", json.dumps({
            "lats" : self.lats,
            "longs" : self.lons,
            "counter" : self.counter
        }))

    def on_message(self, mqttc, obj, msg):
        data = json.loads(msg.payload.decode())
        print(data)

        lat = data['lat']
        lon = data['lon']
        azimuth = data['azimut']

        distance = self.calculate_distance(lat, lon, self.lats[self.counter-1], self.lons[self.counter-1])
        heading = self.calculate_heading(lat, lon, self.lats[self.counter-1], self.lons[self.counter-1])

        if self.form is not None:
            self.form.log_value.set(  ("\n" + str(data)))
            self.form.lat_value.set(lat)
            self.form.coordinate_value.set(azimuth)
            self.form.long_value.set(lon)
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
            
        adj_azimuth = (azimuth + 360) % 360
        adj_heading = adj_azimuth - heading
        if adj_heading < 0:
            adj_heading += 360

        self.inputs = adj_heading
        error = self.setpoint - self.inputs
        if error > 180: 
            error -= 360
        elif error < -180:
            error += 360

        current_time = 10
        # dt = current_time - self.previous_time
        # self.integral += error * dt
        # derivative = (error - self.previous_error) / dt

        # output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        # self.previous_error = error
        # self.previous_time = current_time

        # servo_angle = 90 - output
        # servo_angle = max(0, min(servo_angle, 180))
        if distance < 2.5:
            self.counter += (1 if self.counter  <= len(self.lats)else 0)
            if self.form is not None : self.form.counter_value.set(str(self.counter))

        res =  json.dumps({
            "distance": distance,
            "adjHeading": adj_heading,
            "adjAzm": adj_azimuth,
            "setpoint": self.setpoint,
            "counter": self.counter,
            "lat2" : self.lats[self.counter-1],
            "long2" : self.lons[self.counter-1],
            "motor" : self.motor,
            "speed" : self.speed if self.counter < len(self.lats) else 1550
        })
        if self.form is not None: self.form.log_res.set(str(res))
        mqttc.publish("data/result",res)
            

    def on_subscribe(self, mqttc, obj, mid, reason_code_list):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))
       

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setForm(self, form):
        self.form = form


mymqtt = myMqtt()
async def mqtt():
    mqttc = mymqtt.mqttc
    mqttc.connect_async("192.168.1.4", 1883)
    mqttc.subscribe("sensor/data", 0)
    thread = threading.Thread(target=mqttc.loop_forever)
    thread.start()


asyncio.run(mqtt())



