#imports
import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector

#variables
width, height = 1280, 720
folderpath='Presentation'
imgaeNumber=0
hs,ws=150,250
gestureThreshold=300
buttonPresed=False
buttonCounter=0
buttonDelay=20
annotations=[[]]
annotationNumber=0
annotationStart=False

#getting input from camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pathImages = sorted(os.listdir(folderpath),key=len)

#Hand Detector
detector=HandDetector(detectionCon=0.8,maxHands=1)
    
#During Execution
while True:
    #accesing feed from camera and importing images
    flag, img = cap.read()
    pathFullImage=os.path.join(folderpath,pathImages[imgaeNumber])
    currImage=cv2.imread(pathFullImage)
    img=cv2.flip(img,1)
    
    #detcting hand during runtime and operations
    hands,img=detector.findHands(img,flipType=False)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)
    
    if hands and buttonPresed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        lmlist=hand["lmList"]
        xVal=int(np.interp(lmlist[8][0],[width//2,width],[0,width]))
        yVal=int(np.interp(lmlist[8][1],[150,height-150],[0,height]))
        indexFinger=xVal,yVal
                
        #Only checking gestutres above line
        if cy<=gestureThreshold:
            #Gesture-1 Go Forward
            if fingers==[1,0,0,0,0]:
                if imgaeNumber<len(pathImages)-1:
                    imgaeNumber+=1  
                    buttonPresed=True
                    annotations=[[]]
                    annotationNumber=0
                    annotationStart=False
            
            #Gesture-2 Go back
            if fingers==[0,0,0,0,1]:
                if imgaeNumber>0: 
                    imgaeNumber-=1 
                    buttonPresed=True
                    annotations=[[]]
                    annotationNumber=0
                    annotationStart=False   
                    
        #Gesture-3 Pointer
        if fingers==[0,1,0,0,0]: 
            cv2.circle(currImage, indexFinger,12,(0,0,255),cv2.FILLED)
        
        #Gesture-4 Draw
        if fingers==[0,1,1,0,0]:
            if annotationStart is False:
                annotationStart=True
                annotationNumber+=1
                annotations.append([]) 
            cv2.circle(currImage, indexFinger,12,(0,0,255),cv2.FILLED)                        
            annotations[annotationNumber].append(indexFinger)
        
        else:
            annotationStart=False
            
        #Gesture-5 Eraser
        if fingers==[0,1,1,1,0]:
            if annotations:
                if annotationNumber>-1:
                    annotations.pop(-1)
                    annotationNumber-=1
                    buttonPresed=True
    
    else:
        annotationStart=False             
            
    #Adding Delay b/w inputs
    if buttonPresed:
        buttonCounter+=1
        if buttonCounter>buttonDelay:
            buttonCounter=0
            buttonPresed=False
    
    #Drawing Line
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(currImage,annotations[i][j-1],annotations[i][j],(0,0,200),12)
            
    
    #display user img on top of slide
    imgSmall=cv2.resize(img,(ws,hs))
    h,w,_=currImage.shape
    currImage[0:hs,w-ws:w]=imgSmall   
      
    
    #showing output
    cv2.imshow("Slide", currImage)
    # cv2.imshow("Image", img)
    
    #condition to close
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
