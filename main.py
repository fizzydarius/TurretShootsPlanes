#import libaries
import cv2
import numpy as np

#Setting up the capture
cap = cv2.VideoCapture(0)

def emtpy(x):
    pass

#Creating track bar to help track a certain colour
#In my testing case I'm using an orange debit card
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0,179,emtpy)
cv2.createTrackbar("HUE Max", "HSV", 0,179,emtpy)
cv2.createTrackbar("SAT Min", "HSV", 0,255,emtpy)
cv2.createTrackbar("SAT Max", "HSV", 0,255,emtpy)
cv2.createTrackbar("VALUE Min", "HSV", 0,255,emtpy)
cv2.createTrackbar("VALUE Max", "HSV", 0,255,emtpy)


#Loop to detect plane
while True:

    #Telling the program to record from webcam
    ret, frame = cap.read()

    #Creating a new Colourspace in HSV which makes it easeir for computers to see colours
    ImageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Getting infromation from the trackbar window "HSV" and storing it into variables as integers 
    h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max","HSV")
    s_min = cv2.getTrackbarPos("SAT Min","HSV")
    s_max = cv2.getTrackbarPos("SAT Max","HSV")
    v_min = cv2.getTrackbarPos("VALUE Min","HSV")
    v_max = cv2.getTrackbarPos("VALUE Max","HSV")
    
    #Setting the upper and lower bounadries as arrays 
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    # output the lower values and upper values of the sliders:: print (lower,upper)
    #Create a mask on the ImageHSV colour-space with the lower and upper limits set on the trackbar.
    mask = cv2.inRange(ImageHSV, lower, upper)
    #Get the results, combine the original colour-space and the HSV colour-space and output only the things that are the same
    results = cv2.bitwise_and(frame,frame, mask = mask)
    
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #sorting the contour based of area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    if contours:
        #if any contours are found we take the biggest contour and get bounding box
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])
        #drawing a rectangle around the object with 15 as margin
        cv2.rectangle(frame, (x_min - 15, y_min -15),
                      (x_min + box_width + 15, y_min + box_height + 15),
                      (0,255,0), 4)
        print (x_min,y_min,box_height,box_width)
        # Drew on a paper and realsed the middle is the x_min,y_min plus half of the boxes width and height respectfully
        # the big question is do i make it round or does it just cut up before it reaches decimal points (aka turn it into an int)
        x_coord = int(x_min+(box_width/2))
        y_coord = int(y_min+(box_height/2))
        cv2.circle(frame,(x_coord,y_coord),radius=2,color=(0,0,255),thickness=1)


    hStack = np.hstack([frame,results ])

    #Show the camera outputs
    #cv2.imshow('Original', frame) #Normal Camera
    #cv2.imshow('hsv frame', ImageHSV) #HSV camera
    #cv2.imshow("mask", mask)
    #cv2.imshow("Results", results)
    cv2.imshow("horizontal stacking of result and original", hStack)
    #When pressed break loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Released and closes the capture windows for the webcam
cap.release()
cv2.destroyAllWindows()