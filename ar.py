import serial

arduinoData = serial.Serial("COM3",9600)

def __init__():
    arduinoData.write(b"LR")
    arduinoData.write(b"LY")

def red_led_on():
    arduinoData.write(b"HR")

def yellow_led_on():
    arduinoData.write(b"HY")

