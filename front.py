from tkinter import *
import cv2
import pickle
import cvzone
import numpy as np

class Smart_Parking_System:
    def __init__(self, root):
        self.root = root
        print("hello")
        self.root.geometry("100x100+0+0")
        self.root.title("Smart Parking")



    #    bg_img = Label(self.root, image=self.photoimg)
    #    bg_img.place(x=50, y=500, width=1700, height=910)

    def parking(self):
        cap = cv2.VideoCapture(2)

        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)

        width, height = 107, 48

        def checkParkingSpace(imgPro):
            spaceCounter = 0

            for pos in posList:
                x, y = pos

                imgCrop = imgPro[y:y + height, x:x + width]
                # cv2.imshow(str(x * y), imgCrop)
                count = cv2.countNonZero(imgCrop)

                if count < 900:
                    color = (0, 255, 0)
                    thickness = 5
                    spaceCounter += 1
                else:
                    color = (0, 0, 255)
                    thickness = 2

                cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
                cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                                   thickness=2, offset=0, colorR=color)

            cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (0, 50), scale=3,
                               thickness=5, offset=20, colorR=(0, 0, 0))
            if spaceCounter > 0:
                cvzone.putTextRect(img, f'There : {spaceCounter} Free lines', (390, 50), scale=4,
                                   thickness=5, offset=20, colorR=(0, 0, 0))

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

            #checkParkingSpace(imgDilate)
            cv2.imshow("Image", img)
            cv2.waitKey(10)




if __name__ == "__main__":
    root = Tk()
    obj = Smart_Parking_System(root)
    root.mainloop()