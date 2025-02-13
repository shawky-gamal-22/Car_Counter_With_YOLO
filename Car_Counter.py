from ultralytics import YOLO
import cv2
import cvzone
import math
import torch
from sort import *


print("YOLO running on:", "GPU" if torch.cuda.is_available() else "CPU")


cap = cv2.VideoCapture('../Videos/cars.mp4')

mask = cv2.imread('mask.png')

model = YOLO("../Yolo_Weights/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

tracker = Sort(max_age= 20, min_hits= 3, iou_threshold= 0.3)
limits = [400, 297, 673, 297]
totalCount = []
while True:
    success, img = cap.read()
    imgRegion = cv2.bitwise_and(img,mask)
    results = model(imgRegion,stream=True)

    imGraphics = cv2.imread('graphics.png',cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img,imGraphics,(0,0))

    detection = np.empty((0,5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(0,200,0),3)

            # bounding box
            w , h = x2 - x1 , y2 - y1


            # confidence level
            conf = math.ceil((box.conf[0]*100))/100
            #cvzone.putTextRect(img,f'{conf}',(max(0,x1),max(35,y1)))

            # class name you should have the list of the names of the classes and take the index from the yolo and drow it
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if currentClass == "car" or currentClass == "truck" or currentClass == "bus"\
                    or currentClass == "motorbike" and conf >  0.3:
                #cvzone.cornerRect(img, (x1, y1, w, h), l=9)
                #cvzone.putTextRect(img,f'{classNames[cls]} {conf}', (max(0,x1),max(35,y1)),
                                #scale =0.6,thickness=1,offset=3)
                currentArray = np.array([[x1,y1,x2,y2,conf]])
                detection = np.vstack((detection,currentArray))


    resultsTracker = tracker.update(detection)
    # This is the line if the center of the detection move on it it will be counted
    cv2.line(img,(limits[0],limits[1]),(limits[2],limits[3]),(255,0,0),3)


    for result in resultsTracker:
        x1,y1,x2,y2,Id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(result)
        w,h = x2-x1,y2-y1
        cvzone.cornerRect(img,(x1,y1,w,h),l=9, rt=2, colorR=(255,0,255))
        cvzone.putTextRect(img,f'ID {int(Id)}', (max(0,x1),max(35,y1)),
                        scale =2,thickness=3,offset=10)
        # Center of Detection
        cx,cy = x1+w//2,y1+h//2
        cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        # If the center move on the region of the line
        if limits[0] < cx < limits[2] and limits[1]-15 < cy < limits[3]+15:
            if int(Id) not in totalCount:
                totalCount.append(int(Id))
                # Change the line color to green if the car move on it
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 3)


    #cvzone.putTextRect(img, f'Count: {len(totalCount)}', (50,50))
    cv2.putText(img,str(len(totalCount)),(255,100), cv2.FONT_HERSHEY_PLAIN,5,(50,50,255),8)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
