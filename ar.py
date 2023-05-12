import serial


class Arduino():
    def __init__(self):
        self.dataWrite = serial.Serial("COM3",9600)
        print("started")

    def coord(self, x_coord, y_coord):
        """minRangeX = 90 - (70.42/2)
        maxRangeX = 90 + (70.42/2)
        minRangeY = 90 - (43.30/2)
        maxRangeY = 90 + (43.30/2)"""
        midPoint = 90

        xVal = 1920/70.42
        yVal = 1080/43.30
        x_coord = 90 + (x_coord-960)/xVal
        y_coord = 90 + (y_coord-540)/yVal
        x_coord = round(x_coord)
        y_coord = round(y_coord)

        self.send_message(x_coord, y_coord)
        return (x_coord, y_coord)

    def send_message(self, x, y):
        data = bytes([255, x, y, 254], encoding="utf-8")
        self.dataWrite.write(data)

