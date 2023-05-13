#imports of libraries and modular scripts
import cv2
import numpy as np
from tkinter import *
import multiprocessing as mp
import json
import ar

# main video capturing feed class
class visualRecognition():

    def __init__(self, a, b , c , d , e ,f):
        # initialiasion of the set up for the camera and start arduino script
        self.cap = cv2.VideoCapture(0)
        self.arduino = ar.Arduino()
        self.guiWindow = False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.windowOpen = True

        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = a , b , c , d , e , f

        self.createWindow()
    
    # Image Recognition code and function
    def empty(self,x):
        pass

    def createWindow(self):
        #create the Hue Saturation and Value trackbar window where you can calibrate
        cv2.namedWindow("HSV")
        cv2.resizeWindow("HSV", 600, 260)
        cv2.createTrackbar("HUE Min", "HSV", self.lastH_min,179,self.empty)
        cv2.createTrackbar("HUE Max", "HSV", self.lastH_max,179,self.empty)
        cv2.createTrackbar("SAT Min", "HSV", self.lastS_min,255,self.empty)
        cv2.createTrackbar("SAT Max", "HSV", self.lastS_max,255,self.empty)
        cv2.createTrackbar("VALUE Min", "HSV", self.lastV_min,255,self.empty)
        cv2.createTrackbar("VALUE Max", "HSV", self.lastV_max,255,self.empty)

        self.windowOpen = True

    def destroyWindow(self):
        # store the last known values within the variables (they go into an empty container because class was initilised in an if statement once) then close all windows
        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, 
        self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
        cv2.destroyAllWindows()
        self.windowOpen = False


    def windowOptions(self):
        # Q = close everything , A = hide windows, keep loop running , D = Show windows
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "stopLoop"
        if cv2.waitKey(1) & 0xFF == ord('a'):
            self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, 
            self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
            cv2.destroyAllWindows()
            self.windowOpen = False
            return "runLoop"
        if cv2.waitKey(1) & 0xFF == ord('d'):
            self.createWindow()
            return "runLoop"
        
    def trackbarPos(self):
        
        # get the value for the trackbars and store them
        if self.windowOpen == True:
            self.lastH_min = cv2.getTrackbarPos("HUE Min","HSV")
            self.lastH_max = cv2.getTrackbarPos("HUE Max","HSV")
            self.lastS_min = cv2.getTrackbarPos("SAT Min","HSV")
            self.lastS_max = cv2.getTrackbarPos("SAT Max","HSV")
            self.lastV_min = cv2.getTrackbarPos("VALUE Min","HSV")
            self.lastV_max = cv2.getTrackbarPos("VALUE Max","HSV")


        # create a lower and upper array to be used to make bounds 
        self.lower = np.array([self.lastH_min,self.lastS_min,self.lastV_min])
        self.upper = np.array([self.lastH_max,self.lastS_max,self.lastV_max])
        #print((f"{self.lower}, {self.upper}")) this was used for testing

    def main(self):
        #main loop
        while True:
            # turn on the camera, and mask what you see based on the values of the trackbar
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, None, None, fx=0.5, fy=0.5) # change to 1 when window closed
            ImageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            self.trackbarPos()
            mask = cv2.inRange(ImageHSV, self.lower, self.upper)
            results = cv2.bitwise_and(frame, frame, mask = mask) 
            contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            #draws a rectange around the biggest area seen and a circle in the middle, outputs the degrees at which the 
            # turret should point at, this was caluclated through the arduino communication script
            if contours:
                (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])

                cv2.rectangle(frame,
                              (x_min - 15, y_min - 15),
                              (x_min + box_width + 15, y_min + box_height + 15),
                              (0,255,0),
                              4)
                x_coord = int(x_min+(box_width/2))
                y_coord = int(y_min+(box_height/2))
                cv2.circle(frame,(x_coord,y_coord),radius=2,color=(0,0,255),thickness=1)
                print(self.arduino.coord(x_coord,y_coord))

            #show results
            hStack = np.hstack([frame,results])

            if self.windowOpen == True:
                cv2.imshow("hello world", hStack)
                cv2.waitKey(1)
            if self.windowOptions() == "stopLoop":
                # when window closes, store the values in a .json file
                dictionary = {
                    "hmin": f"{self.lastH_min}",
                    "hmax": f"{self.lastH_max}",
                    "smin": f"{self.lastS_min}",
                    "smax": f"{self.lastS_max}",
                    "vmin": f"{self.lastV_min}",
                    "vmax": f"{self.lastV_max}"
				}
                with open("sample.json", "w") as outfile:
                     json.dump(dictionary, outfile)
                
                break
			
            
        self.cap.release()
        cv2.destroyAllWindows()



class GraphicalUserInterface():
    def __init__(self):
        #variables
        self.motorButtonClicked = False



        #main window configurations and settings
        self.window = Tk()
        self.window.geometry("800x400")
        self.window.title("Turret shoots planes")
        icon = PhotoImage(file="car.png")
        self.window.iconphoto(True, icon)
        self.window.config(background="#5b98c7")

        self.window.grid_columnconfigure(0, minsize = 40)
        self.window.grid_columnconfigure(2, minsize = 60)

        #buttons 
        self.hardButton = Button(self.window,
                text="Hard",
                padx = "100",
                command= lambda: self.hardMode(),
                font=("Comic Sans",30),
                fg="black",
                bg="#c72828",
                activeforeground="black",
                activebackground="#a62121")
        self.hardButton.grid(row=0,column=2,columnspan=2,padx=(0,30),pady=(40,0))

        self.easyButton = Button(self.window,
                text="Easy",
                padx = "100",
                command= lambda: self.easyMode(),
                font=("Comic Sans",30),
                fg="black",
                bg="#319e3c",
                activeforeground="black",
                activebackground="#236e2b")
        self.easyButton.grid(row=0,column=5,columnspan=2,pady=(40,0))

        self.motorButton = Button(self.window,
                text = "Motor",
                command= lambda: self.motorButtonColourChange(),
                font=("Comic Sans",30),
                fg="black",
                bg="#a62121",
                activebackground="#a62121")
        self.motorButton.grid(row=1,column=6,pady=(40,0))

        self.calibrationButton = Button(self.window,
                text = "Calibration",
                command = lambda: self.calibrationMode(),
                font = ("Comic Sans", 30),
                fg = "black",
                bg = "#eb7134",
                activebackground= "#c25d2b")
        self.calibrationButton.grid(row=2, column=6, pady=(40,0))

        #labels
        self.MotorLabel = Label(self.window,
            text="Motor mode: OFF",
            font=("Calibri 15 bold"),
            bg="#5b98c7")
        self.MotorLabel.grid(row=2,column=2)


        self.ModeStatus = Label(self.window,
            text="Difficulty mode: Easy",
            font=('Calibri 15 bold'),
            bg="#5b98c7")
        self.ModeStatus.grid(row=1,column=2, pady=(100,0))

    #start the loop
    def startWindow(self):
        self.window.mainloop()

    #Changes the colour for the motor button
    def motorButtonColourChange(self):
        if self.motorButtonClicked == False:
            print(f"Motor is activated!")
            self.motorButton["bg"] = "#319e3c"
            self.motorButtonClicked = True
            self.MotorLabel["text"] = "Motor mode: ON"
            self.motorButton["activebackground"] = "#236e2b"

        elif self.motorButtonClicked == True:
            print(f"Motor is deactivated!")
            self.motorButton["bg"] = "#c72828"
            self.motorButtonClicked = False
            self.MotorLabel["text"] = "Motor mode: OFF"
            self.motorButton["activebackground"] = "#a62121"

    def calibrationMode(self):
        # read the .json file and initalise the video capturing loop using the values for the Hue, Saturation and Value
        data = json.load(open('sample.json'))
        a = int(data['hmin'])
        b = int(data['hmax'])
        c = int(data['smin'])
        d = int(data['smax'])
        e = int(data['vmin'])
        f = int(data['vmax'])
        visualRec = visualRecognition(a, b , c , d , e , f)
        # attempt to use multiprocessing in order to run the two main loops asycronically
        program = mp.Process(target= visualRec.main(), args=())
        program.start()

    def hardMode(self):
        print(f"Hard mode is activated!")
        self.ModeStatus["text"] = "Difficulty mode: Hard"

    def easyMode(self):
        print(f"Easy mode activated!")
        self.ModeStatus["text"] = "Difficulty mode: Easy"

if __name__ == "__main__":
    gui = GraphicalUserInterface()
    #attempt to use multiprocessing in order to run the two main loops asycronically
    program2 = mp.Process(target= gui.startWindow(), args=())
    program2.start()
    program2.join()


