import cv2
import numpy as np
from tkinter import *


class visualRecognition():

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.windowOpen = True
        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = 0 , 0 , 0 , 0 , 0 , 0
    
        self.createWindow()

    def createWindow(self):
        self.windowOpen = True

    def destroyWindow(self):
        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
        cv2.destroyAllWindows()
        self.windowOpen = False
        
    def main(self):
        while True:
            ret, frame = self.cap.read()
            #code here to get results and draw a nice rectangle :)
            hStack = np.hstack([frame,results])

            if self.windowOpen == True:
                cv2.imshow("hello world", hStack)
                cv2.waitKey(1)


class GraphicalUserInterface():
    def __init__(self):
        
        #variables
        self.calibrationButtonClicked = False
        self.calibrationCounter = 0 
        #main window configurations and settings
        self.window = Tk()

        self.calibrationButton = Button(self.window,
                text = "Calibration",
                command = lambda: self.calibrationMode(),
                font = ("Comic Sans", 30),
                fg = "black",
                bg = "#eb7134",
                activebackground= "#c25d2b")
        self.calibrationButton.grid(row=2, column=6, pady=(40,0))

        self.window.mainloop()


    def calibrationMode(self):
        if self.calibrationCounter == 0:
            visualRec = visualRecognition()
            visualRec.main()
            self.calibrationButtonClicked = True
            self.calibrationCounter += 1
            print(f"Initial calibration in progress")
        else:
            if self.calibrationButtonClicked == False:
                self.calibrationButtonClicked = True
                visualRec.createWindow()
                print(f"Calibration in progress")

            elif self.calibrationButtonClicked == True:
                self.calibrationButtonClicked = False
                visualRec.destroyWindow()
                print(f"Calibration over")

if __name__ == "__main__":
    GraphicalUserInterface()

