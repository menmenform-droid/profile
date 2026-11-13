import urllib.request
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

urls = [
    ('https://eastcoast.chinapress.com.my/20210207/%E2%97%A4%E7%9C%8B%E8%A7%86%E9%A2%91%E2%97%A2%E5%8A%A0%E7%B4%A7%E4%B8%8E%E5%8D%8E%E8%A3%94%E9%97%B4%E7%9A%84%E8%81%94%E7%B3%BB-%E6%A2%81%E4%B8%9A%E6%B5%B7%E8%A2%AB%E5%A7%94%E4%BB%BB%E8%8B%B1/', 'appointment'),
    ('https://www.enanyang.my/news/20180121/State/104482', 'bookshelf'),
    ('https://eastcoast.sinchew.com.my/news/20210716/eastcoast/3237267', 'foodbasket'),
    ('https://www.enanyang.my/news/20170921/State/116746', 'prison'),
    ('https://eastcoast.chinapress.com.my/20211019/%E8%B5%9B%E5%A4%AB%E4%B8%81%EF%BC%9A%E5%9B%BD%E5%AE%B6%E6%9C%AA%E6%9D%A5%E4%B8%BB%E4%BA%BA%E7%BF%81-%E9%9D%92%E5%B0%91%E5%B9%B4%E6%84%8F%E8%A7%81-%E5%BA%94%E8%8E%B7%E9%87%8D%E8%A7%86/', 'taekwondo'),
    ('https://eastcoast.chinapress.com.my/20200324/%E6%8D%90%E5%8F%A3%E7%BD%A9%E6%90%93%E6%89%8B%E6%B6%B2%E5%8A%A9%E9%98%B2%E7%96%AB-%E4%BC%81%E4%B8%9A%E8%B5%A0%E5%89%8D%E7%BA%BF%E4%BA%BA%E5%91%98%E7%89%A9%E8%B5%84/', 'donation'),
    ('https://www.sinchew.com.my/20190426/%E4%B8%8A%E6%B5%B7%E6%96%87%E5%8C%96%E4%BD%BF%E8%80%85%EF%BC%8E%E5%90%91%E5%85%89%E5%8D%8E%E7%94%9F%E6%8E%A8%E5%B9%BF%E9%98%85%E8%AF%BB/', 'shanghai')
]

os.makedirs('images', exist_ok=True)

for url, label in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Find og:image
            og_img = re.search(r'<meta[^>]*property=[\"\']og:image[\"\'][^>]*content=[\"\']([^\"\']+)[\"\']', html, re.I)
            if not og_img:
                og_img = re.search(r'<meta[^>]*content=[\"\']([^\"\']+)[\"\'][^>]*property=[\"\']og:image[\"\']', html, re.I)
            
            all_imgs = re.findall(r'<img[^>]*src=[\"\']([^\"\']+)[\"\']', html, re.I)
            
            target_img = None
            if og_img and ('chinapress' in og_img.group(1) or 'sinchew' in og_img.group(1) or 'enanyang' in og_img.group(1) or 'uploads' in og_img.group(1)):
                target_img = og_img.group(1)
            else:
                for img in all_imgs:
                    if any(x in img.lower() for x in ['upload', 'content', 'article', 'wp-content']) and not any(x in img.lower() for x in ['logo', 'icon', 'advertisement', 'banner']):
                        target_img = img
                        break
                if not target_img and og_img:
                    target_img = og_img.group(1)
            
            print(f'=== {label} ===')
            print('Selected Image:', target_img)
            
            if target_img:
                if target_img.startswith('//'):
                    target_img = 'https:' + target_img
                img_req = urllib.request.Request(target_img, headers=headers)
                ext = target_img.split('?')[0].split('.')[-1].lower()
                if len(ext) > 4 or ext not in ['jpg', 'jpeg', 'png', 'webp']:
                    ext = 'jpg'
                filename = f'images/{label}.{ext}'
                with urllib.request.urlopen(img_req, timeout=15) as img_resp, open(filename, 'wb') as f:
                    f.write(img_resp.read())
                print(f'Successfully downloaded to {filename} ({os.path.getsize(filename)} bytes)')
    except Exception as e:
        print(f'Error for {label}: {e}')
