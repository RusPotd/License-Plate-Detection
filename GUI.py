from tkinter import *
import threading
import time


global URL, Display
URL = False
Display = False


def some_video():
    while(True):
        if(Display == False):
            break
        print("Running Infinite loop")
        time.sleep(1)

def stop():
    global STOP
    print("Stop : STOP = True")
    STOP = True

def setDisplay():
    global Display
    print("setDisplay : Display = True")
    Display = True

def resetDisplay():
    global Display
    print("resetDisplay : Display = False")
    Display = False

def seturl():
    global URL
    print("seturl : URL = True")
    URL = True

def play(event):
    print("Inside Play")

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

    print("Cam : "+str(cam))
    Display = True

    t = threading.Thread(target=some_video)      #Parallel Processing
    t.start()
    
  #functions

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
