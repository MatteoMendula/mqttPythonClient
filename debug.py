"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit


# Each Pulse Width Modulation (PWM) Pin corresponds to a motor
# PWM 0 - 6 : doors
# PWM 8 - 15 : windows
# 00 : Bedroom 2 - Bathroom
# 01 : Bedroom 1 - Living Rm
# 02 : Living Rm - Kitchen
# 03 : Living Rm - Bathroom
# 04 : Bedroom 1 - Bathroom
# 05 : Living Rm - Front Door
# 06 : Bedroom 1 - Back Door

# 08 : Bedroom 1, 2 ft.
# 09 : Living Rm, 2 ft.
# 10 : Bedroom 2, 2 ft
# 11 : Kitchen, 2 ft.
# 12 : Bedroom 2, 3 ft.
# 13 : Living Rm, 3 ft.
# 14 : Kitchen, 3 ft.
# 15 : Bedroom 1, 3 ft.


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

def closeMotor(pin):
    kit.servo[pin].angle = getClosingAngle(pin)
def openMotor(pin):
    kit.servo[pin].angle = getOpeningAngle(pin)
def closeMotorCustom(pin,closing_angle):
    kit.servo[pin].angle = closing_angle
def openMotorCustom(pin,opening_angle):
    kit.servo[pin].angle = opening_angle
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
    try:
        while (True):
            openMotor(pin)
            time.sleep(5)
            closeMotor(pin)
            time.sleep(5)
    except KeyboardInterrupt:
    	print("Keyboard interrupt.")
    	GPIO.cleanup()
    
    
    

while(True):
    try:
        while (True):
            print('Enter desired operation')
            op = input().lower()
            words = op.split()
            if op == 'open all':
                print("opening all doors and windows")
                openAll()
            elif op == 'close all':
                print("closing all doors and windows")
                closeAll()
            elif op == 'open all doors':
                print("opening all doors")
                openAllDoors()
            elif op == 'close all doors':
                print("closing all doors")
                closeAllDoors()
            elif op == 'open all windows':
                print("opening all windows")
                openAllWindows()
            elif op == 'close all windows':
                print("closing all windows")
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
                print('Incorrect input.')
    except KeyboardInterrupt:
    	print("Keyboard interrupt.")
    	GPIO.cleanup()

