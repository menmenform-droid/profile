from PIL import Image
import os

for f in sorted(os.listdir('images')):
    p = os.path.join('images', f)
    if os.path.isfile(p):
        try:
            im = Image.open(p)
            print(f, im.size, im.format)
        except Exception as e:
            print(f, 'error:', e)
