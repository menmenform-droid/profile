import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = 'http://sukabaca-sukatulis.blogspot.com/2016/10/mbs-world-kedai-buku-terbesar-di-pantai.html'
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        print('Imgs:', imgs)
        for img in imgs:
            if 'blogger' in img or 'bp.blogspot' in img:
                with urllib.request.urlopen(img) as r, open('images/mbs_world.jpg', 'wb') as f:
                    f.write(r.read())
                print('Saved mbs_world.jpg successfully!')
                break
except Exception as e:
    print('Err:', e)
