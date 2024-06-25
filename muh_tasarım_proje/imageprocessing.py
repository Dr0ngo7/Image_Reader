import cv2
import numpy as np
import easyocr as ocr

reader = ocr.Reader(['tr','en'],gpu=True)
def rec(img):
    #filtrelemeler
    #gray dönüşüm
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #eşikleme
    img_thresh = cv2.threshold(img_gray, 95, 155, cv2.THRESH_BINARY)[1]
    
    yazilar = reader.readtext(img_thresh)
    
    for yazi in yazilar:
        cv2.rectangle(img,[int(yazi[0][0][0]),int(yazi[0][0][1])], [int(yazi[0][2][0]),int(yazi[0][2][1])],(0,255,0), 2)
    
    
    for(box, metin,deger) in yazilar:
        print(f"metin: {metin}, güvenirlilik: {deger:.2f}")
    







'''
reader = ocr.Reader(['tr','en'])
img = cv2.imread(adres)



#renk tersleme
#img = cv2.bitwise_not(img)

#grültü giderme 
#img = cv2.medianBlur(img, 5)
#img = cv2.bilateralFilter(img,9,75,75)

#eşikleme
img_thresh = cv2.threshold(img_gray, 95, 155, cv2.THRESH_BINARY)[1]

yazilar = reader.readtext(img_thresh)

#for yazi in yazilar:
  #  print(yazi)

for yazi in yazilar:
    cv2.rectangle(img,[int(yazi[0][0][0]),int(yazi[0][0][1])], [int(yazi[0][2][0]),int(yazi[0][2][1])],(0,255,0), 2)
#result = reader.readtext(img)

for(box, metin,deger) in yazilar:
    print(f"metin: {metin}, güvenirlilik: {deger:.2f}")
'''