import cv2
import os

for f in ['appointment.jpg', 'foodbasket.png', 'taekwondo.jpg', 'shanghai.jpeg']:
    p = os.path.join('images', f)
    img = cv2.imread(p)
    print(f, 'loaded successfully, shape:', img.shape)
