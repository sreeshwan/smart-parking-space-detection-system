import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture(2)

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 95, 40


def checkParkingSpace(imgPro):
    spaceCounter = 0
    
    i = 0
    close = []

    for pos in posList:
        x, y = pos
        
        i +=1

        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            close.append(i)
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(i), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    
    
    #print(close)
    
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (200, 30), scale=1,
                           thickness=1, offset=10, colorR=(0,0,0))
    cvzone.putTextRect(img, f'Entry', (0, 30), scale=1,
                           thickness=1, offset=10, colorR=(0, 0, 0))
    if spaceCounter>0:
        cvzone.putTextRect(img, f'Closest Parking slot : {close[0]}', (430, 30), scale=1,
                           thickness=1, offset=10, colorR=(0, 0, 0))
    if close[0]<9:
        start_point = (150, 100) 
        end_point = (150, 200)
        color = (0, 0, 255)
    
        cv2.arrowedLine(img, start_point, end_point,  
                    color, thickness, tipLength = 0.5)
    else:
        start_point = (460, 100) 
        end_point = (460, 200)
        color = (0, 0, 255)
    
        cv2.arrowedLine(img, start_point, end_point,  
                    color, thickness, tipLength = 0.5)
        
        start_point = (300, 60) 
        end_point = (400, 60)
        color = (0, 0, 255)
    
        cv2.arrowedLine(img, start_point, end_point,  
                    color, thickness, tipLength = 0.3)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
        
    checkParkingSpace(imgDilate)
    
#    for pos in posList:
#        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 0, 255), 1)
    
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)   
    cv2.resizeWindow("Image", 1200, 800)
    cv2.imshow("Image", img)
    #cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThreshold", imgThreshold)
    #cv2.imshow("ImageMedian", imgMedian)
    #cv2.imshow("ImgDilate", imgDilate)
    cv2.waitKey(10)
    
  
    #checkParkingSpace(imgDilate)
    
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
