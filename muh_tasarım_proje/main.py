import easyocr as ocr
import cv2
import numpy as np


def is_number_empty(roi):
    """
    Bu fonksiyon, bölgenin (roi) içinin boş olup olmadığını kontrol eder.
    Basit bir piksel yoğunluğu kontrolü yapar.
    """
    # Bölgedeki beyaz piksel oranını kontrol edin
    num_white_pixels = np.sum(roi == 255)
    total_pixels = roi.size
    white_pixel_ratio = num_white_pixels / total_pixels

    # Eğer beyaz piksel oranı belirli bir eşiğin üzerindeyse (örn. %80) bu bölgeyi boş kabul edin
    return white_pixel_ratio > 0.8

adres = r"Resim_verileri\Dogalgaz_sayaci\gaz4.jpg"

reader = ocr.Reader(['tr','en'],gpu=True)
img = cv2.imread(adres)


#gray dönüşüm
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  



#grültü giderme 
img = cv2.medianBlur(img_gray, 5)
#img = cv2.bilateralFilter(img,9,75,75)


#eşikleme

img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


yazilar = reader.readtext(img_thresh)

for (bbox, metin, deger) in yazilar:
    if metin.isdigit():
        # Koordinatları alın
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

        # Sayının bulunduğu bölgeyi alın
        roi = img_thresh[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Eğer sayı boşsa, doldurun
        if is_number_empty(roi):
            cv2.rectangle(img_thresh, top_left, bottom_right, (0, 0, 0), thickness=cv2.FILLED)

degisikyazilar = reader.readtext(img_thresh)
for yazi in degisikyazilar:
    cv2.rectangle(img_thresh,[int(yazi[0][0][0]),int(yazi[0][0][1])], [int(yazi[0][2][0]),int(yazi[0][2][1])],(0,255,0), 2)
  
##result = reader.readtext(img_thresh)
for(box, metin,deger) in degisikyazilar:
    print(f"metin: {metin}, güvenirlilik: {deger:.2f}")

  

##cv2.imshow("test", img)
##cv2.waitKey(0)
cv2.imshow("test", img_thresh)
cv2.waitKey(0)

cv2.destroyAllWindows()


