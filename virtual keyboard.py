import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep
# from pynput.keyboard import Key, Controller 

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

detector = HandDetector(0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""

button_list = []

def draw_all(img,button_list):  
    for button in button_list:
        x,y=button.pos
        w,h = button.size
        cv.rectangle(img,button.pos,(x+w,y+h),(0,0,0),cv.FILLED)
        cv.putText(img, button.text,(x+20,y+65),cv.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 5)  
    return img    

class button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text
            
    

for i in range(len(keys)):
     for j,key in enumerate(keys[i]) :
        button_list.append(button([j*100 + 50,100*i+50],key))


while True:
    ret, img = cap.read()
    img = detector.findHands(img)
    lm_list,bbinfo = detector.findPosition(img)
    img = draw_all(img,button_list)
    
    if lm_list:
        for button in button_list:
            x, y = button.pos
            w, h = button.size   
                     
            #clicked
            if x < lm_list[8][0] < x+w and y<lm_list[8][1]<y+h:
                cv.rectangle(img,button.pos,(x+w,y+h),(0,0,255),cv.FILLED)
                cv.putText(img, button.text,(x+20,y+65),cv.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 5)  
                
                l,_,_= detector.findDistance(8,12,img,draw=False)
                print(l)
                
                if l<40:
                    cv.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv.FILLED)
                    cv.putText(img, button.text,(x+20,y+65),cv.FONT_HERSHEY_SIMPLEX,3,(255,255,255), 5)                 
                    finalText += button.text
                    sleep(0.15)
                    
    cv.rectangle(img,(40,350),(1050,452),(0,0,0),cv.FILLED)
    cv.putText(img, finalText,(60,430),cv.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 5)  
                    
        
    cv.imshow("Image",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break