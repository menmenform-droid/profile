import cv2

img = cv2.imread('images/appointment.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
print('Faces detected in appointment.jpg:', len(faces))
for (x, y, w, h) in faces:
    print('Face:', x, y, w, h)
