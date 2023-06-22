import cv2
import numpy as np
import face_recognition



#link to the article on how the face_recognition package works on the backed sides
#https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78



# loading the image from directory
imgN = face_recognition.load_image_file('imageBasics/narendraModi.jpg')
# converting the image as rgb which is in bgr
imgN = cv2.cvtColor(imgN,cv2.COLOR_BGR2RGB)

imgNTest = face_recognition.load_image_file('imageBasics/narendraModiTest.jpg')
imgNTest = cv2.cvtColor(imgNTest,cv2.COLOR_BGR2RGB)


#locate the face in the picture and it will return 4 values top,right,bottom and left
faceLoc=face_recognition.face_locations(imgN)[0]
print(faceLoc)
#encoding the face we have detected
encodeN=face_recognition.face_encodings(imgN)[0]

# to see where we have detected the faces
# rectangle(imageName,left points, right points, color, width)
cv2.rectangle(imgN,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,0),2)

#encoding the testing image
encodeNTest=face_recognition.face_encodings(imgNTest)[0]

results=face_recognition.compare_faces([encodeN],encodeNTest)
# to find the best match we will find the distance, lower the distance better the match
faceDis=face_recognition.face_distance([encodeN],encodeNTest)

print(results,faceDis)
cv2.putText(imgNTest,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)


#opening a window with pictures and window name
cv2.imshow('Narendra Modi',imgN)
cv2.imshow('Narendra Modi Test',imgNTest)
cv2.waitKey(0)


