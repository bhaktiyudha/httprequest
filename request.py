import requests
import json
import dateutil.parser
import paho.mqtt.client as mqtt
import time

# publish callback function
def on_publish(client, userdata, result):
    print("data published \n")
    pass

def mqtt_publish(data):
    mqtt_topic = "environment_sensor"
    mqtt_broker_ip = "34.87.119.216"
    client = mqtt.Client()
    client.username_pw_set("jeager", password='Telkom123')                   
    client.connect(mqtt_broker_ip, 1883)
    # assign publish callback function
    client.on_publish = on_publish
    client.publish(mqtt_topic,data)
    

def request(x):
    client_id = "5df30e114ccd8b1af4e5cc7b"
    BASE_URL = "https://platform.antares.id:8443/~/antares-cse/antares-id/EMS-JGR/EMSnode"+str(x)+"/la"
    headers = {
        "X-M2M-Origin": "access-id:access-password",
        "Content-Type": "application/json;ty=4",
        "Accept": "application/json"
    }
    response = requests.get(BASE_URL, headers=headers)
    convert_quotes = str(response.json()).replace("'",'"')
    payload = json.loads(convert_quotes)
    data = (payload['m2m:cin']['con']).split(",")
    time = dateutil.parser.parse(payload['m2m:cin']['ct'])
    temp = data[0]
    hum = data[1]
    device_id = data[2]
    data = parse_data(client_id,device_id,temp,hum,time)
    print (data)
    mqtt_publish(data)

#Fungsi untuk menyimpan data sensor dalam format data yang ditentukan dalam bentuk JSON
def parse_data(client_id,device_id,temperatur,kelembapan,time): 
    payload = {}
    payload_temperatur = {}
    payload_kelembapan = {}
    payload_temperatur['sensor_name'] = 'temperatur'
    payload_temperatur['value'] = float(temperatur)
    payload_kelembapan['sensor_name'] = 'kelembapan'
    payload_kelembapan['value'] = float(kelembapan)
    payload['client_id'] = str(client_id)
    payload['device_id'] = str(client_id) + "-" + str(device_id)
    payload['sensors'] = payload_temperatur,payload_kelembapan
    payload['time']= str(time) + ".000 +0700" 
    return (json.dumps(payload))

while True:
    try:
        for x in range(1, 3):
            request(x)
            time.sleep(1)
    except :
        print ("error")