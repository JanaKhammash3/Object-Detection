import cv2
import numpy as np
import matplotlib as plt
import math

Image = cv2.imread('OriginalImage.jpg')
#turn image into gray scale
img_gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

def function1(approx, contour):   
    
    x, y, w, h = cv2.boundingRect(contour)
    div = float(w) / h
    y = int(y + (h/9)) #y coordinate
    x= int(x + (w/7))  # x coordinate
    #if shape is triangle
    if len(approx) == 3:
        cv2.putText( Image, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )
    #if shape is square
    elif len(approx) == 4:
        if 1.07 >= div >= 0.91:

            cv2.putText( Image, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )
        else:
            cv2.putText( Image, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )

    elif len(approx) >= 10:
        H = cv2.convexHull(contour, returnPoints=False)
        Def = cv2.convexityDefects(contour, H)
        for z in range(Def.shape[0]):
            st, en, f, c = Def[z, 0]
            EN = tuple(contour[en][0]) 
            ST = tuple(contour[st][0]) 
              
        dir = math.sqrt(pow(ST[0] - EN[0], 3) + pow(ST[1] - EN[1], 3)) 
        
        if cv2.arcLength(contour, False) > dir and not(isCls(ST[0], EN[0]) or isCls(ST[1], EN[1])):
            return 'Curve'
        else:
            if 1.06 >= div >= 0.91:
                #shape is curve
                cv2.putText( Image, "Curve", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )
            else:
                #shape is circle
                cv2.putText( Image, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )
    else:
        cv2.putText( Image, "Line", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0) )


def isCls(v1, v2): 

    value = v1 - v2
    if -5 <= value <= 5:
        return True
    else:
        return False


def function2(contour):   
    x1, y1, w1, h1 = cv2.boundingRect(contour)

    for x in range(len(arr)):
        if y1 == arr[3 * x + 0] or y1 == arr[3 * x + 1]:
            return 'Eye'
        elif y1 == arr[3 * x + 2]:
            #if its nose
            return 'Nose'
        else:
            #if mouth
            return 'Mouth'

for cont in contours:
    if cv2.contourArea(cont) > 100:   
        x, y, w, h = cv2.boundingRect(cont)

        apprx = cv2.approxPolyDP(cont, 0.002 * cv2.arcLength(cont, True), True)

        cv2.drawContours(img_gray, cont, -2, (255, 255, 255), 10)
        CrImage= img_gray [y:y+h, x:x+w]   
        facecont, _ = cv2.findContours(CrImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)   
        if len(facecont) > 10:   

            cv2.putText(Image, "Face", (x-2, y+25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)

            arr = []  
                #to set the position
            ret, thresh = cv2.threshold(CrImage, 220, 255, cv2.THRESH_BINARY_INV)
            contoursone, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for contour in contoursone:
                apprx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                arr.append(y1)

            arr.sort(reverse=False)  

            for cont1 in contoursone:
                x1, y1, w1, h1 = cv2.boundingRect(cont1)
                print(x1, y1)
                s1 = function2(cont1)
                cv2.putText(Image, s1, (x1+x, y1+y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                
        else:   #if its not face (what shape?)
            string = function1(apprx, cont)
            
            cv2.putText(Image, string, (apprx.ravel()[0] - 40, apprx.ravel()[1] + 10),
                       cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)

cv2.imshow('shapes', Image)
cv2.waitKey(0)
cv2.destroyAllWindows()