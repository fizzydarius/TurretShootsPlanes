import serial

arduinoData = serial.Serial("com3",9600)

def led_on():
    arduinoData.write(b"1")

def led_off():
    arduinoData.write(b"0")

led_on()