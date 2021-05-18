from tkinter import *
import cv2, os, copy
import threading
import numpy as np
import imutils
import easyocr
import sqlite3



#define globals and getting data ready

global URL, Display
URL = False
Display = False

str_1 = str()

list_1 = []
tup = tuple()

try:
    os.mkdir("Dataset")
except:
    pass

#https://www.youtube.com/watch?v=fgx5LDOx4JY&ab_channel=AnirudhTech make your own haars
cascade = cv2.CascadeClassifier("license.xml")
reader = easyocr.Reader(['en'])

state_code = {
    "AN" : "Andaman and Nicobar Islands", "AP" : "Andhra Pradesh", "AR" : "Arunachal Pradesh", "AS" : "Assam",
    "BR" : "Bihar", "CH" : "Chandigarh", "CT" : "Chhattisgarh", "DN" : "Dadra and Nagar Haveli	",
    "DD" : "Daman and Diu", "DL" : "Delhi", "GA" : "Goa",
    "GJ" : "Gujarat", "HR" : "Haryana", "HP" : "Himachal Pradesh", "JK" : "Jammu and Kashmir", "JH" : "Jharkhand",
    "KA" : "Karnataka", "KL" : "Kerala", "LD" : "Lakshadweep", "MP" : "Madhya Pradesh", "MH" : "Maharashtra",
    "MN" : "Manipur", "ML" : "Meghalaya", "MZ" : "Mizoram", "NL" : "Nagaland", "OR" : "Odisha",
    "PY" : "Puducherry", "PB" : "Punjab", "RJ" : "Rajasthan", "SK" : "Sikkim", "TN" : "Tamil Nadu",
    "TG" : "Telangana", "TR" : "Tripura", "UP" : "Uttar Pradesh", "UT" : "Uttarakhand", "WB" : "West Bengal"
}


#start of functions

def view_frame_video():  #main function -> data preprocessing and operations
    conn = sqlite3.connect('LicenseInfo.db')

    global video, cam

    video = cv2.VideoCapture(cam)

    a = 1; count = 0
    while True:
        if (URL == True):
            #image = cv2.imread('Cars.png')                       #incase of image uncomment this
            #frame = imutils.resize(image, width=500)
            video = cv2.VideoCapture(cam)

        check, frame = video.read()
        duplicateFrame = copy.deepcopy(frame)
        threshold = preprocess(frame)

        nplate = cascade.detectMultiScale(threshold, 1.1, 4)

        c = 0
        num = 1

        for (x, y, w, h) in nplate:
            a, b = (int(0.02 * duplicateFrame.shape[0]), int(0.025 * duplicateFrame.shape[1]))
            plate = duplicateFrame[y + a: y + h - a, x + b:x + w - b, :]

            kernel = np.ones((1, 1), np.uint8)
            plate = cv2.dilate(plate, kernel, iterations=1)
            plate = cv2.erode(plate, kernel, iterations=1)

            try:
                plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            except:
                break
            cv2.rectangle(duplicateFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.imshow('Plate', plate)
            cv2.imwrite('Dataset\license_plate'+str(num)+'.png', plate_gray)

            plate = cv2.imread('Dataset\license_plate'+str(num)+'.png')
            plate = cv2.resize(plate, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            retval, threshold = cv2.threshold(plate, 127, 255, cv2.THRESH_BINARY)

            read = reader.readtext(threshold)
            try:
                read = read[0][-2]
            except:
                break
            print(read+"\n")
            code = read[0:2]
            if code in state_code:
                print("Vehicle belongs to "+state_code[code]+" state\n")
            else:
                print("State not recognized\n")

            cursor = conn.execute("SELECT ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber from Holders")

            plateNo = read[(len(read)-4):len(read)]

            try:
                for row in cursor:
                    if(row[0]==int(plateNo)):
                        print("License Plate No = ", row[0])
                        print("NAME = ", row[1])
                        print("GENDER = ", row[2])
                        print("DOB = ", row[3])
                        print("ADDRESS = ", row[4])
                        print("PhoneNumber = ", row[5])
                        print("\n\n\n")
            except:
                ''' '''

            cv2.rectangle(duplicateFrame, (x, y - 40), (x + w, y), (0, 255, 0), 3)
            cv2.putText(duplicateFrame, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        if (Display == True):
            cv2.imwrite('Dataset\plate' + str(num) + '.png', duplicateFrame)
            path = 'Dataset\plate' + str(num) + '.png'

            pht = PhotoImage(file=path)
            l6.config(width=700,height=400,image=pht)
            l6.image=pht
            os.remove('Dataset\plate' + str(num) + '.png')

        if (STOP == True):
            video.release()
            break

        num += 1

    conn.close()

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    return gray

def stop():
    global STOP

    STOP = True

def setDisplay():
    global Display
    Display = True

def resetDisplay():
    global Display
    Display = False

def seturl():
    global URL
    URL = True

def play(event):

    global cam, URL, STOP, Display
    STOP = False

    #cam = "https://192.168.0.106:8080/shot.jpg"

    if (URL == True):
        cam = entry2.get()
    else:
        cam = entry1.get()
        try:
            cam = int(cam)
            """ """
        except:
            cam = 0

    Display = True

    #view_frame_video()

    t = threading.Thread(target=view_frame_video)      #Parallel Processing
    t.start()

root=Tk()

root.geometry("") # auto resize

root.title('License Plate Detection Software')

#<---------------camera_!------------------------->
l1=Label(root,text="CAMERA1")
l1.grid(row=1,column=1,padx=00,pady=20)

entry1=Entry(root)
entry1.grid(row=1,column=5,padx=10,pady=20)

#<------------------View and off -------------------->


b=Button(root,text="START",height=1,width=8)
b.grid(row=1,column=8,padx=20,pady=15)
b.bind('<Button-1>', play)

b1=Button(root,text="STOP",command=stop,height=1,width=8)
b1.grid(row=1,column=10,padx=10,pady=15)

#<-----------------url ------------------------------>

lb=Label(root,text="URL")
lb.grid(row=2,column=1,padx=10,pady=00)

entry2=Entry(root)
entry2.grid(row=2,column=5,padx=10,pady=00)

b3=Button(root,text="PUSH",command=seturl,height=1,width=8)
b3.grid(row=2,column=8,padx=20,pady=00)

b4=Button(root,text="VIEW",command=setDisplay,height=1,width=8)
b4.grid(row=2,column=10,padx=10,pady=15)

b5=Button(root,text="PAUSE",command=resetDisplay,height=1,width=8)
b5.grid(row=2,column=12,padx=10,pady=15)


#<---------------------------Entries of Min&Max height and width---------------------->

l6=Label(root,text="Your Camera will be displayed here",bd=3,borderwidth=2, relief="groove",height=30, width=100)
l6.grid(row=11,rowspan=15, columnspan=30,sticky=W,pady=50,padx=25)

root.mainloop()



