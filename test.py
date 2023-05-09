class visualRecognition():

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.windowOpen = True

        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = 0 , 0 , 0 , 0 , 0 , 0
    
        self.createWindow()

    # Image Recognition code and function
    def empty(self,x):
        pass

    def createWindow(self):
        #creates trackbar
        self.windowOpen = True

    def destroyWindow(self):
        self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
        cv2.destroyAllWindows()
        self.windowOpen = False
        
    def windowOptions(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "stopLoop"
        if cv2.waitKey(1) & 0xFF == ord('a'):
            self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max = self.lastH_min, self.lastH_max, self.lastS_min, self.lastS_max, self.lastV_min, self.lastV_max
            cv2.destroyAllWindows()
            self.windowOpen = False
            return "runLoop"
        if cv2.waitKey(1) & 0xFF == ord('d'):
            self.createWindow()
            return "runLoop"
        
    def trackbarPos(self):
        
        if self.windowOpen == True:
            #gets position of trackbar 

        self.lower = np.array([self.lastH_min,self.lastS_min,self.lastV_min])
        self.upper = np.array([self.lastH_max,self.lastS_max,self.lastV_max])
        #print((f"{self.lower}, {self.upper}"))

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
                #draws a rectangle from bounds and prints x-y coords

            hStack = np.hstack([frame,results])

            if self.windowOpen == True:
                cv2.imshow("hello world", hStack)

        self.cap.release()
        cv2.destroyAllWindows()
