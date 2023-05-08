import cv2
import numpy as np

class visualRecognition():

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.windowOpen = True

        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = 0 , 0 , 0 , 0 , 0 , 0
    
        self.createWindow()

    def empty(self,x):
        pass

    def createWindow(self):
        cv2.namedWindow("HSV")
        cv2.resizeWindow("HSV", 600, 260)
        cv2.createTrackbar("HUE Min", "HSV", self.lastH_min,179,self.empty)
        cv2.createTrackbar("HUE Max", "HSV", self.lastH_max,179,self.empty)
        cv2.createTrackbar("SAT Min", "HSV", self.lastS_min,255,self.empty)
        cv2.createTrackbar("SAT Max", "HSV", self.lastS_max,255,self.empty)
        cv2.createTrackbar("VALUE Min", "HSV", self.lastV_min,255,self.empty)
        cv2.createTrackbar("VALUE Max", "HSV", self.lastV_max,255,self.empty)
        self.windowOpen = True

    def windowOptions(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "stopLoop"
        if cv2.waitKey(1) & 0xFF == ord('a'):
            self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
            cv2.destroyWindow("HSV")
            self.windowOpen = False
            return "runLoop"
        if cv2.waitKey(1) & 0xFF == ord('d'):
            self.createWindow()
            return "runLoop"
        
    def trackbarPos(self):
        
        if self.windowOpen == True:
            print(f"window is open")
            self.lastH_min = cv2.getTrackbarPos("HUE Min","HSV")
            self.lastH_max = cv2.getTrackbarPos("HUE Max","HSV")
            self.lastS_min = cv2.getTrackbarPos("SAT Min","HSV")
            self.lastS_max = cv2.getTrackbarPos("SAT Max","HSV")
            self.lastV_min = cv2.getTrackbarPos("VALUE Min","HSV")
            self.lastV_max = cv2.getTrackbarPos("VALUE Max","HSV")

        self.lower = np.array([self.lastH_min,self.lastS_min,self.lastV_min])
        self.upper = np.array([self.lastH_max,self.lastS_max,self.lastV_max])
        print((f"{self.lower}, {self.upper}"))

    def main(self):
        while True:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, None, None, fx=0.5, fy=0.5) # change to 1 when window closed
            ImageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            self.trackbarPos()
            mask = cv2.inRange(ImageHSV, self.lower, self.upper)
            results = cv2.bitwise_and(frame, frame, mask = mask)
            contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

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
                print(f"{x_coord}, {y_coord}")

            hStack = np.hstack([frame,results])

            cv2.imshow("hello world", hStack)

            if self.windowOptions() == "stopLoop":
                break
        self.cap.release()
        cv2.destroyAllWindows()

app = visualRecognition()
app.main()