import paho.mqtt.client as mqtt
import time
from adafruit_servokit import ServoKit

#-------------------------------- SERVO KIT
kit = ServoKit(channels=16)

def closeMotor(pin):
    kit.servo[pin].angle = getClosingAngle(pin)
def openMotor(pin):
    kit.servo[pin].angle = getOpeningAngle(pin)
def getClosingAngle(pin):
    if pin == 10 or pin == 12 or pin == 15:
        return 50
    elif pin == 11:
        return 55
    else:
        return 60
def getOpeningAngle(pin):
    if pin == 15:
        return 160
    else:
        return 180
    
def openAll():
    for x in range(0, 16):
        openMotor(x)        
def closeAll():
    for x in range(0, 16):
        closeMotor(x)
def closeAllDoors():
    for x in range(0, 7):
            closeMotor(x)         
def closeAllWindows():
    for x in range(8, 16):
            closeMotor(x)           
def openAllDoors():
    for x in range(0, 7):
            openMotor(x)        
def openAllWindows():
    for x in range(8, 16):
            openMotor(x)
def loopMotor(pin):
    openMotor(pin)
    time.sleep(5)
    closeMotor(pin)
    time.sleep(5)
    openMotor(pin)
    time.sleep(5)
    closeMotor(pin)
    time.sleep(5)
    
        
#-------------------------------- MQTT
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    msg_raw = str(msg.payload)
    #print('[log matte - msg payload raw]: '+str(msg.payload))
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msg_cleaned = msg_raw[2:len(msg_raw)-1]
    print('[LOG - from topic '+ msg.topic +' - msg payload cleaned]: '+str(msg_cleaned))
    words = msg_cleaned.split()
    if msg_cleaned == "open all":
        print('Opening all doors')
        openAll()
    elif msg_cleaned == "close all":
        print('Closing all doors')
        closeAll()
    elif msg_cleaned == 'open all doors':
        print("Opening all doors")
        openAllDoors()
    elif msg_cleaned == 'close all doors':
        print("Closing all doors")
        closeAllDoors()
    elif msg_cleaned == 'open all windows':
        print("Opening all windows")
        openAllWindows()
    elif msg_cleaned == 'close all windows':
        print("Closing all windows")
        closeAllWindows()
    elif words[0] == 'open':
        #open based on pin number
        print("opening motor " + words[1])
        '''
        if words[1] == '15':
            openMotorCustom(15,160)
        else:
        '''
        openMotor(int(words[1]))
    elif words[0] == 'close':
        #close based on pin number
        print("closing motor " + words[1])
        '''
        if words[1] == '15':
            closeMotorCustom(15,50)
        elif words[1] == '10':
            closeMotorCustom(10,50)
        elif words[1] == '11':
            closeMotorCustom(11,55)
        elif words[1] == '12':
            closeMotorCustom(12,50)
        else:
        '''
        closeMotor(int(words[1]))
    elif words[0] == 'loop':
        print("looping motor " + words[1])
        loopMotor(int(words[1]))
    else:
        print('Unknown command')

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
#url_str = 'mqtt://m12.cloudmqtt.com:11110'
#url = urlparse.urlparse(url_str)
url = 'm12.cloudmqtt.com'
port = 11110
topic = 'scaledhome'

# Connect
#mqttc.username_pw_set(url.username, url.password)
mqttc.username_pw_set('actuatorcontroller', 'actuator')
mqttc.connect(url, port)

# Start subscribe, with QoS level 0
mqttc.subscribe(topic, 2)

# Publish a message
mqttc.publish(topic, "my message")

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))