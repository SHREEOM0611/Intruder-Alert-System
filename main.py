import cv2
import numpy as np
import face_recognition

import os
import ssl
import csv
from datetime import datetime

import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from email.message import EmailMessage
# import win32com.client
email_sender = 'omshree.osj18705@gmail.com'
email_password = 'pilkgvxpwccwaimm'
email_receiver = 'omshree.osj74404@gmail.com'

subject = '!!!!!!!!INTRUDER ALERT!!!!!!!'
# outlook = win32com.client.Dispatch('outlook.application')


path = 'imageAttendance'
# taking the images from a folder
images=[]
# taking the name of the person from images
classNames = []
myList = os.listdir(path)
# print(myList)

# To get the names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# print(classNames)

# function to encode the images

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# call the function to encode the images
encodeListKnown = findEncodings(images)
print(' Encoding completed ')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  #resizing the image as bigger in size they are more time it will take
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)      #encoded the image taken from webcam


    # as we can detect multiple faces in the webcam so we will findout the location of the faces and send these locations for the encoding
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    flag = 0
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)   # it will give the list of distances and the lower distances will be the best match
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        print(matches)
        if matches[matchIndex]:
            flag = flag+1
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1=faceLoc
            y1, x2, y2, x1= y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
        # else:
        #     flag = 0
        #     print("Intruder")
        #     y1, x2, y2, x1 = faceLoc
        #     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #     cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        #     cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
        #     cv2.putText(img, "INTRUDER", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


    if flag == 0:
        cv2.imwrite('intruder1.jpeg', imgS)

        content = """
         This is a warning!!! 
         There's an intruder in your house.
        """
        em = MIMEMultipart()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        body = MIMEText(content, 'plain')
        em.attach(body)

        filename='intruder1.jpeg'

        with open(filename, 'r') as f:
            attachment = MIMEApplication(f.read(), Name=basename(filename))
            attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
        em.attachment(filename);
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())



        print("flag=")
        print(flag)


    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
