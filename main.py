import cv2
import numpy as np
import time
from cvzone.HandTrackingModule import HandDetector
import HandTrackingModulePaint as Phtm
import os
import csv
import cvzone
from pynput.keyboard import Controller
from HandTrackingModuleKeyboard import HandDetectorK
from time import sleep
from playsound import playsound
from threading import Thread
import winsound
import pyttsx3

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetectorK(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()
engine = pyttsx3.init()
flag1 = 1
engine.say("Please enter your name without using your Physical Keyboard")
engine.setProperty('rate', 50)

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        #print(button.pos)
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 50, rt=0, colorC = (0, 0, 255))
        cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (0, 255, 255), 3)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 4)
    return img

def hello(x):
	#only for referece
	print("")

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

EnterButton = []

EnterButton.append(Button((830, 400), "Enter", [200, 100]))



global boolflag
boolflag=0

def Playsongbeep():
    frequency = 2500
    duration = 500
    winsound.Beep(frequency, duration)



# def PlaysongIntro():
#     playsound('welcome.mp3')


def PlayEnterBeep():
    frequency = 1000
    duration = 1000
    winsound.Beep(frequency, duration)






def cheers():
    playsound('D:\\Coding\\Python\\Komaldeep virtual world\\sounds\\cheers.wav')

flagT=1

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
    img = drawAll(img,EnterButton)
    EnterFlag = 0
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (255, 0, 0), 4)
                cv2.putText(img, button.text, (x + 20, y + 65),  cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)
                l, _, _ = detector.findDistance(4, 8, img, draw=False)
                #Thread(target=PlayHoverBeep).start()
                #sleep(0.15)




                if l < 40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 255), 4)
                    finalText += button.text
                    Thread(target=Playsongbeep).start()

                    sleep(0.15)

            xe, ye = EnterButton[0].pos
            we, he = EnterButton[0].size
            if xe < lmList[8][0] < xe + we and ye < lmList[8][1] < ye + he:
                cv2.rectangle(img, (xe - 5, ye - 5), (xe + we + 5, ye + he + 5), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "Enter", (xe + 20, ye + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 255), 4)
                le, _, _ = detector.findDistance(4, 8, img, draw=False)


                if le < 40:
                    cv2.rectangle(img, tuple(EnterButton[0].pos), (xe + we, ye + he), (0, 255, 0), cv2.FILLED)
                    EnterFlag = 1
                    Thread(target=PlayEnterBeep).start()
                    break

    cv2.rectangle(img, (50, 400), (800, 500), (0, 255, 255), 4)
    cv2.putText(img, finalText, (60, 475), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if flagT == 1:
        engine.runAndWait()
        flagT = 0
    if(EnterFlag==1):
        break


BackToMenu = 0






detecthand = 1

while True:
    success, imgvq = cap.read()
    imgvq = cv2.flip(imgvq, 1)
    if detecthand==1:
        detector = HandDetectorK(detectionCon=0.8)
        detecthand=0
    imgvq = detector.findHands(imgvq)
    lmListQuiz, bboxInfoQuiz = detector.findPosition(imgvq)




    MenuQuestionRecSp = [40, 40]
    MenuQuestionRecEp = [1100, 100]
    MenuQuestionTxtSp = [50, 80]
    cv2.rectangle(imgvq, tuple(MenuQuestionRecSp), tuple(MenuQuestionRecEp), (0, 255, 255), 5)
    MenuQuestion = "Welcome " + finalText + ", What do you want to do?"
    cv2.putText(imgvq, MenuQuestion, tuple(MenuQuestionTxtSp), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    Option1RecSp = [40, 200]
    Option1RecEp = [550, 400]
    Option1TxtSp = [50, 315]
    cv2.rectangle(imgvq, tuple(Option1RecSp), tuple(Option1RecEp), (0, 255, 255), 5)
    cv2.putText(imgvq, "Play virtual Quiz", tuple(Option1TxtSp), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    Option2RecSp = [600, 200]
    Option2RecEp = [1110, 400]
    Option2TxtSp = [650, 315]
    cv2.rectangle(imgvq, tuple(Option2RecSp), tuple(Option2RecEp), (0, 255, 255), 5)
    cv2.putText(imgvq, "Play Music", tuple(Option2TxtSp), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    Option3RecSp = [40, 500]
    Option3RecEp = [550, 700]
    Option3TxtSp = [50, 615]
    cv2.rectangle(imgvq, tuple(Option3RecSp), tuple(Option3RecEp), (0, 255, 255), 5)
    cv2.putText(imgvq, "Do some magic", tuple(Option3TxtSp), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    Option4RecSp =[600, 500]
    Option4RecEp = [1110, 700]
    Option4TxtSp = [650, 615]
    cv2.rectangle(imgvq, tuple(Option4RecSp), tuple(Option4RecEp), (0, 255, 255), 5)
    cv2.putText(imgvq, "Let's Paint", tuple(Option4TxtSp), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)

    #Now hands ki position detect karni hai


    if lmListQuiz:
        print(lmListQuiz[8][0], lmListQuiz[8][1])
        #Virtual quiz vala option implement karne ja rha hu
        if 40 < lmListQuiz[8][0] < 550 and 200 < lmListQuiz[8][1] < 400:

            cv2.rectangle(imgvq, (40, 200), (550 + 5, 400 + 5), (0, 255, 0), 4)
            cv2.putText(imgvq, "Play virtual Quiz", (50, 315), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
            lop1, _, _ = detector.findDistance(4, 8, imgvq, draw=False)


            if lop1 < 40:

                cv2.rectangle(imgvq, (40, 200), (550 + 5, 400 + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgvq, "Play virtual Quiz", (50, 315), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)



                cv2.destroyAllWindows()
                cap.set(3, 1280)
                cap.set(4, 720)
                detector2 = HandDetector(detectionCon=0.8)
                detector = HandDetectorK()


                class MCQ():
                    def __init__(self, data):
                        self.question = data[0]
                        self.choice1 = data[1]
                        self.choice2 = data[2]
                        self.choice3 = data[3]
                        self.choice4 = data[4]
                        self.answer = int(data[5])

                        self.userAns = None

                    def update(self, cursor, bboxs):

                        for x, bbox in enumerate(bboxs):
                            x1, y1, x2, y2 = bbox
                            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                                self.userAns = x + 1
                                cv2.rectangle(img, (x1, y1), (x2, y2), (255,0 , 0), 5)


                # Importing csv file data
                pathCSV = "Mcqs.csv"
                with open(pathCSV, newline='\n') as f:
                    reader = csv.reader(f)
                    dataAll = list(reader)[1:]

                # Har MCQ k liye ek ek object bnaya hai
                mcqList = []
                for q in dataAll:
                    mcqList.append(MCQ(q))

                print("Total MCQ Objects Created:", len(mcqList))

                qNo = 0
                qTotal = len(dataAll)

                while True:
                    success, img = cap.read()
                    img = cv2.flip(img, 1)
                    hands, img = detector2.findHands(img)

                    if qNo < qTotal:
                        mcq = mcqList[qNo]

                        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, (0, 0, 0), (255, 255, 255), offset=50, border = 5)
                        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, (0, 0, 0), (255, 255, 255), offset=50, border=5)
                        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [600, 250], 2, 2, (0, 0, 0), (255, 255, 255), offset=50, border=5)
                        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, (0, 0, 0), (255, 255, 255), offset=50, border=5)
                        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [600, 400], 2, 2, (0, 0, 0), (255, 255, 255), offset=50, border=5)

                        if hands:
                            lmList = hands[0]['lmList']
                            cursor = lmList[8]
                            length, info = detector2.findDistance(lmList[4], lmList[8])
                            #print(length)
                            if length < 35:
                                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                                if mcq.userAns is not None:
                                    time.sleep(0.3)
                                    qNo += 1
                    else:
                        score = 0
                        for mcq in mcqList:
                            if mcq.answer == mcq.userAns:
                                score += 1
                        score = round((score / qTotal) * 100, 2)
                        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
                        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)
                        cv2.rectangle(img, (0, 0), (200, 100), (0, 0, 255), cv2.FILLED)
                        cv2.putText(img, "Main Menu", (0, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                        Thread(target=cheers).start()

                        # Exit button
                        if hands:
                            lmList = hands[0]['lmList']
                            cursor = lmList[8]

                            if 0 < lmList[8][0] < 200 and 0 < lmList[8][1] < 100:
                                cv2.destroyAllWindows()
                                print("YES")
                                BackToMenu = 1
                                detecthand = 1
                                break

                    #Progress Bar
                    barValue = 150 + (950 // qTotal) * qNo
                    cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
                    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
                    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)
                    # Exit button





                    cv2.imshow("Img", img)
                    cv2.waitKey(1)

        elif 40 < lmListQuiz[8][0] < 550 and 500 < lmListQuiz[8][1] < 700:
            cv2.rectangle(imgvq, (40, 500), (550 + 5, 700 + 5), (255, 0, 0), 4)
            cv2.putText(imgvq, "Do some magic", (50, 615), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
            lop1, _, _ = detector.findDistance(4, 8, imgvq, draw=False)


            if lop1 < 40:
                cv2.rectangle(imgvq, (40, 500), (550 + 5, 700 + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgvq, "Do some magic", (50, 615), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)

                cv2.destroyAllWindows()




                bars = cv2.namedWindow("bars")

                cv2.createTrackbar("upper_hue", "bars", 110, 180, hello)
                cv2.createTrackbar("upper_saturation", "bars", 255, 255, hello)
                cv2.createTrackbar("upper_value", "bars", 255, 255, hello)
                cv2.createTrackbar("lower_hue", "bars", 93, 180, hello)
                cv2.createTrackbar("lower_saturation", "bars", 162, 255, hello)
                cv2.createTrackbar("lower_value", "bars", 120, 255, hello)
                time.sleep(5)
                # Capturing the initial frame for creation of background
                while (True):
                    cv2.waitKey(1000)
                    ret, init_frame = cap.read()
                    # check if the frame is returned then brake
                    if (ret):
                        break

                # Start capturing the frames for actual magic!!
                # init_frame = cv2.imread("init_frame.jpg", cv2.IMREAD_COLOR)
                while (True):
                    ret, frame = cap.read()
                    inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    # getting the HSV values for masking
                    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
                    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
                    upper_value = cv2.getTrackbarPos("upper_value", "bars")
                    lower_value = cv2.getTrackbarPos("lower_value", "bars")
                    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
                    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")

                    # Kernel to be used for dilation
                    kernel = np.ones((3, 3), np.uint8)

                    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
                    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])

                    mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
                    mask = cv2.medianBlur(mask, 3)
                    mask_inv = 255 - mask
                    mask = cv2.dilate(mask, kernel, 5)

                    # The mixing of frames in a combination to achieve the required frame
                    b = frame[:, :, 0]
                    g = frame[:, :, 1]
                    r = frame[:, :, 2]
                    b = cv2.bitwise_and(mask_inv, b)
                    g = cv2.bitwise_and(mask_inv, g)
                    r = cv2.bitwise_and(mask_inv, r)
                    frame_inv = cv2.merge((b, g, r))

                    b = init_frame[:, :, 0]
                    g = init_frame[:, :, 1]
                    r = init_frame[:, :, 2]
                    b = cv2.bitwise_and(b, mask)
                    g = cv2.bitwise_and(g, mask)
                    r = cv2.bitwise_and(r, mask)
                    blanket_area = cv2.merge((b, g, r))

                    final = cv2.bitwise_or(frame_inv, blanket_area)
                    final = cv2.flip(final, 1)
                    final = detector.findHands(final, draw = False)
                    cv2.rectangle(final, (0, 0), (200, 100), (0, 255, 0), cv2.FILLED)
                    cv2.putText(final, "Main Menu", (0, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)

                    lmListQuiz, bboxInfoQuiz = detector.findPosition(final)
                    if lmListQuiz:
                        print(lmListQuiz[8][0], lmListQuiz[8][1])
                        # Virtual quiz vala option implement karne ja rha hu
                        if 0 < lmListQuiz[8][0] < 200 and 0 < lmListQuiz[8][1] < 100:

                            print("YES")
                            BackToMenu = 1
                            detecthand = 1
                            break
                    cv2.imshow("Magic", final)




                    if (cv2.waitKey(3) == ord('q')):
                        break;

                cv2.destroyAllWindows()


        elif 600 < lmListQuiz[8][0] < 1110 and 500 < lmListQuiz[8][1] < 700:

            cv2.rectangle(imgvq, (600, 500), (1110 + 5, 700 + 5), (255, 0, 0), 4)
            cv2.putText(imgvq, "Let's Paint", (650, 615), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
            lop1, _, _ = detector.findDistance(4, 8, imgvq, draw=False)

            ## when clicked
            if lop1 < 40:
                cv2.rectangle(imgvq, (600, 500), (1110 + 5, 700 + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgvq, "Let's Paint", (650, 615), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)

                overlayList = []  # list to store all the images

                brushThickness = 25
                eraserThickness = 100
                drawColor = (255, 0, 255)  # setting purple color

                xp, yp = 0, 0
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # defining canvas

                                                                   # images in header folder
                folderPath = "Header"
                myList = os.listdir(folderPath)                    # getting all the images used in code
                # print(myList)
                for imPath in myList:                              # reading all the images from the folder
                    image = cv2.imread(f'{folderPath}/{imPath}')
                    overlayList.append(image)                        # inserting images one by one in the overlayList
                header = overlayList[0]                             # storing 1st image

                cap.set(3, 1280)  # width
                cap.set(4, 720)  # height

                detector = Phtm.handDetector(detectionCon=0.50, maxHands=1)  # making object

                while True:

                    # 1. Import image
                    success, img = cap.read()
                    img = cv2.flip(img, 1)  # for neglecting mirror inversion

                    # 2. Find Hand Landmarks
                    img = detector.findHands(img)  # using functions fo connecting landmarks
                    lmList, bbox = detector.findPosition(img, draw=False)  # using function to find specific landmark position,draw false means no circles on landmarks

                    if len(lmList) != 0:
                        # print(lmList)
                        x1, y1 = lmList[8][1], lmList[8][2]  # tip of index finger
                        x2, y2 = lmList[12][1], lmList[12][2]  # tip of middle finger

                        # 3. Check which fingers are up
                        fingers = detector.fingersUp()
                        # print(fingers)

                        # 4. If Selection Mode - Two finger are up
                        if fingers[1] and fingers[2]:
                            xp, yp = 0, 0
                            # print("Selection Mode")
                            # checking for click
                            if y1 < 125:
                                if 250 < x1 < 450:  # if i m clicking at purple brush
                                    header = overlayList[0]
                                    drawColor = (255, 0, 255)
                                elif 550 < x1 < 750:  # if i m clicking at blue brush
                                    header = overlayList[1]
                                    drawColor = (255, 0, 0)
                                elif 800 < x1 < 950:  # if i m clicking at green brush
                                    header = overlayList[2]
                                    drawColor = (0, 255, 0)
                                elif 1050 < x1 < 1200:  # if i m clicking at eraser
                                    header = overlayList[3]
                                    drawColor = (0, 0, 0)
                            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor,
                                          cv2.FILLED)  # selection mode is represented as rectangle

                        # 5. If Drawing Mode - Index finger is up
                        if fingers[1] and fingers[2] == False:
                            cv2.circle(img, (x1, y1), 15, drawColor,
                                       cv2.FILLED)                                                                        # drawing mode is represented as circle
                            # print("Drawing Mode")
                            if xp == 0 and yp == 0:                                                                        # initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                                xp, yp = x1, y1                                                                           # so to avoid that we set xp=x1 and yp=y1
                                                                                                                          # till now we are creating our drawing but it gets removed as everytime our frames are updating so we have to define our canvas where we can draw and show also

                            # eraser
                            if drawColor == (0, 0, 0):
                                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                            else:
                                cv2.line(img, (xp, yp), (x1, y1), drawColor,
                                         brushThickness)  # gonna draw lines from previous coodinates to new positions
                                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                            xp, yp = x1, y1  # giving values to xp,yp everytime

                        # merging two windows into one imgcanvas and img

                    # 1 converting img to gray
                    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)

                    # 2 converting into binary image and thn inverting
                    _, imgInv = cv2.threshold(imgGray, 50, 255,
                                              cv2.THRESH_BINARY_INV)  # on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask

                    imgInv = cv2.cvtColor(imgInv,
                                          cv2.COLOR_GRAY2BGR)  # converting again to gray bcoz we have to add in a RGB image i.e img

                    # add original img with imgInv ,by doing this we get our drawing only in black color
                    img = cv2.bitwise_and(img, imgInv)

                    # add img and imgcanvas,by doing this we get colors on img
                    img = cv2.bitwise_or(img, imgCanvas)

                    # setting the header image
                    img[0:125, 0:1280] = header  # on our frame we are setting our JPG image acc to H,W of jpg images


                    cv2.rectangle(img, (0, 0), (200, 110), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Main Menu", (0, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)

                    lmList, bboxInfo = detector.findPosition(img)
                    if lmList:
                        print(lmList[8][0], lmList[8][1])
                       
                        if 0 < lmList[8][0] < 200 and 0 < lmList[8][1] < 100:
                            print("YES")
                            BackToMenu = 1
                            break

                    cv2.imshow("Image", img)
                    # cv2.imshow("Canvas", imgCanvas)
                    # cv2.imshow("Inv", imgInv)
                    cv2.waitKey(1)


        elif 600 < lmListQuiz[8][0] < 1110 and 200 < lmListQuiz[8][1] < 400:
            cv2.rectangle(imgvq, (600, 200), (1110 + 5, 400 + 5), (255, 0, 0), 4)
            cv2.putText(imgvq, "Play Music", (650, 315), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
            lop1, _, _ = detector.findDistance(4, 8, imgvq, draw=False)

            ## when clicked
            if lop1 < 40:
                cv2.rectangle(imgvq, (600, 200), (1110 + 5, 400 + 5), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgvq, "Play Music", (650, 315), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
                detector4 = HandDetectorK(detectionCon=0.8)


                def Playsong():
                    playsound('D:\\Music\\BornToShine.mp3')

                flag1 = 1
                cv2.destroyAllWindows()

                capture = cv2.VideoCapture('Bvideo.mp4')
                while True:
                    isTrue, frame2 = capture.read()
                    # success1, imgvq1 = cap.read()
                    # imgvq1 = cv2.flip(imgvq1, 1)
                    # imgvq1 = detector4.findHands(img)
                    # cv2.rectangle(imgvq1, (280, 100), (1000 + 5, 500 + 5), (0, 255, 255), 4)
                    #
                    # cv2.putText(imgvq1, "Playing Diljit Dosanjh's", (320, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                    # cv2.putText(imgvq1, ''' "Born to shine "''', (320, 300), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                    # cv2.rectangle(imgvq1, (0, 0), (200, 110), (0, 255, 0), cv2.FILLED)
                    # cv2.putText(imgvq1, "Main Menu", (0, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)

                    # lmList, bboxInfo = detector4.findPosition(imgvq1)
                    # if lmList:
                    #     print(lmList[8][0], lmList[8][1])
                    #
                    #     if 0 < lmList[8][0] < 200 and 0 < lmList[8][1] < 100:
                    #         print("YES")
                    #         BackToMenu = 1
                    #
                    #         break
                    if flag1 == 1:
                        Thread(target=Playsong).start()
                        flag1 = 0

                    # cv2.imshow("imgvq1", imgvq1)

                    #  cv.imshow('Video',frame)
                    cv2.imshow('frame2', frame2)

                    if cv2.waitKey(30) & 0xFF == ord(' '):  # stops video when pressed space
                        BackToMenu=1
                        break

    if(BackToMenu == 1):
         BackToMenu = 0
         continue

    cv2.imshow("Image", imgvq)
    cv2.waitKey(1)


print("DOne")
cv2.destroyAllWindows()
cap.release()