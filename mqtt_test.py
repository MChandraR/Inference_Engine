
import math
import json
import paho.mqtt.client as mqtt
import threading
import asyncio

counter = 1

lats = [
    0.912033,
    0.912028,
    0.912024,
    0.912020,
    0.912015,
    0.912014,
    0.912011
]

lons = [
    104.468216,
    104.468222,
    104.468226,
    104.468223,
    104.468228,
    104.468222,
    104.468213
]

Kp = 1.0
Ki = 0.0
Kd = 0.1

setpoint = 0
inputs = 0
output = 0
integral = 0
previous_error = 0
previous_time = 0

def calculate_heading(lat1, lon1, lat2, lon2):
    delta_lon = lon2 - lon1
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(delta_lon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon))
    
    heading = math.atan2(x, y) * 180.0 / math.pi

    if heading < 0:
        heading += 360.0
    
    return heading

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Radius of Earth in meters

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = math.sin(dLat / 2.0) * math.sin(dLat / 2.0) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2.0) * math.sin(dLon / 2.0)

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return R * c

def on_connect(mqttc, obj, reason_code, properties):
    mqttc.subscribe("sensor/data", 0)
    print("Connected to %s:%s" % (mqttc.host, mqttc.port))

def on_message(mqttc, obj, msg):
    global integral
    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if msg.topic == "sensor/data":
        data = json.loads(msg.payload.decode())
        print(data)
        lat = data['lat']
        latDirection = data['latDirection']
        lon = data['lon']
        lonDirection = data['lonDirection']
        rawLat = data['rawlat']
        rawLon = data['rawlon']
        azimuth = data['azimut']
         
        distance = calculate_distance(lat, lon, lats[0], lons[0])
        heading = calculate_heading(lat, lon , lats[0], lons[0])
        adjAzm = (azimuth + 360) % 360
        adjHeading = adjAzm - heading
        if adjHeading < 0:
            adjHeading  += 360
        inputs = adjHeading 
        setpoint = 0
        error = setpoint - inputs
        if error > 180 : 
            errror -= 360
        elif error < -180:
            error += 360
        current_time = 10.0
        prev_time  =0.0
        prev_error = 0
        dt = (current_time - prev_time) / 1000.0
        integral += error *dt
        derivate = (error-prev_error) / dt
        output = Kp*error  + Ki * integral + Kd * derivate
        previous_error  =  error
        previous_time = current_time
        servoAngle = 90 - output
        servoAngle = max(0, min(servoAngle, 180))
        
        mqttc.publish("data/result", json.dumps({
            "distance " : distance,
            "adjHeading" : adjHeading,
            "adjAzm" : adjAzm,
            "setpoint" : setpoint,
            "servoAngle" : servoAngle,
            "counter" : counter,
            
        }))
        
        


def on_subscribe(mqttc, obj, mid, reason_code_list,):
    print("Subscribed: "+str(mid)+" "+str(reason_code_list))

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log

async def mqtt():
    mqttc.connect_async("192.168.2.121", 1883)
    mqttc.subscribe("sensor/data", 0)
    thread = threading.Thread(target=mqttc.loop_forever)
    thread.start()


asyncio.run(mqtt())



