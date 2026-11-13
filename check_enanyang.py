import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for url, label in [('https://www.enanyang.my/news/20180121/State/104482', 'bookshelf'), ('https://www.enanyang.my/news/20170921/State/116746', 'prison')]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        filtered = [i for i in imgs if any(k in i.lower() for k in ['storage', 'files', 'upload', 'image', 'picture']) and not any(k in i.lower() for k in ['logo', 'icon', 'cover_image', 'banner'])]
        print(label, filtered)
