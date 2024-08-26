
import math
import json
import paho.mqtt.client as mqtt
import threading
import asyncio

class myMqtt:
    def __init__(self) -> None:
        self.counter = 1
        self.lats = [
            0.912033,
            0.912028,
            0.912024,
            0.912020,
            0.912015,
            0.912014,
            0.912011
        ]

        self.lons = [
            104.468216,
            104.468222,
            104.468226,
            104.468223,
            104.468228,
            104.468222,
            104.468213
        ]
        
        self.form = None

        self.Kp = 1.0
        self.Ki = 0.0
        self.Kd = 0.1

        self.setpoint = 0
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
            self.form.lat2_vaule.set(self.lats[self.counter-1])
            self.form.lon2_value.set(self.lons[self.counter-1])
            
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

        mqttc.publish("data/result", json.dumps({
            "distance": distance,
            "adjHeading": adj_heading,
            "adjAzm": adj_azimuth,
            "setpoint": self.setpoint,
            "counter": self.counter,
        }))

    def on_subscribe(self, mqttc, obj, mid, reason_code_list):
        print("Subscribed: " + str(mid) + " " + str(reason_code_list))

    def on_log(self, mqttc, obj, level, string):
        print(string)
        
    def setForm(self, form):
        self.form = form


mymqtt = myMqtt()
async def mqtt():
    mqttc = mymqtt.mqttc
    mqttc.connect_async("192.168.1.105", 1883)
    mqttc.subscribe("sensor/data", 0)
    thread = threading.Thread(target=mqttc.loop_forever)
    thread.start()


asyncio.run(mqtt())



