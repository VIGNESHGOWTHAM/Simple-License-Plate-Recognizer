import cv2
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

frameWidth = 640
frameHeight = 480
nPlateCascade = cv2.CascadeClassifier("cascade/haarcascade_russian_plate_number.xml")
minArea = 200
color = (255,0,255)


cap = cv2.VideoCapture(sys.argv[1])
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

while cap:
    success, img = cap.read()
    if not success:
        cv2.destroyAllWindows()
        break
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            #cv2.putText(img,"LP",(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            imgRoi = img[y:y+h,x:x+w]
            imgroigray = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2GRAY)
            #imgroiblur = cv2.GaussianBlur(imgroigray,(3,3),0)
            #imgroicanny = cv2.Canny(imgroiblur,100,100)
            cv2.imshow("ROI", imgroigray)
            #Read the license plate text
            text = pytesseract.image_to_string(imgroigray, lang='eng', config='--psm 6')
            text = text.replace("[","").replace("]","").replace("(","").replace(")","").replace(":","").replace(";","").replace('"','').replace('|',"").replace("/","").replace("\\","")
            text = text.replace("'","").replace(".","").replace(",","").replace("=","").replace("-","").replace("_","").replace("{","").replace("}","").strip()
            if len(text) >= 4 and len(text) <= 15:
              print("Detected Number is:",text)
              cv2.imwrite("detectedplates/"+text+".jpg",imgroigray)
    cv2.imshow("Input Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
