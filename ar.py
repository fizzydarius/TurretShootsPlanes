import serial


class Arduino():
    def __init__(self):
        self.dataWrite = serial.Serial("COM3",9600)
        # connect to serial with port com3 at 9600 baud
    def coord(self, x_coord, y_coord):
        xVal = 1920/70.42
        yVal = 1080/43.30
        #constant values 

        x_coord = 90 + (x_coord-960)/xVal
        y_coord = 90 + (y_coord-540)/yVal
        x_coord = round(x_coord)
        y_coord = round(y_coord)

        self.send_message(x_coord, y_coord)
        return (x_coord, y_coord)

    def send_message(self, x, y):
        #converting data to bytes so it can be sent over serial 
        data = bytes([255, x, y, 254], encoding="utf-8")
        self.dataWrite.write(data)



