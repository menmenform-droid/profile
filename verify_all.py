import os
import re

with open('leong_yea_hai_profile.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('File size:', len(html), 'bytes')
print('Check 英国法学学士:', '英国法学学士' in html)
print('Check 全马最大综合概念书局:', '全马最大综合概念书局' in html)
print('Check 彭大臣:', '彭大臣' in html)
print('Check 郭小庄:', '郭小庄' in html)
print('Check 拉法儿童之家:', '拉法儿童之家' in html)
print('Check 书山书海:', '书山书海' in html)

imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f'Total images referenced: {len(imgs)}')
for img in imgs:
    exists = os.path.exists(img)
    sz = os.path.getsize(img) if exists else 0
    print(f' - {img}: exists={exists}, size={sz} bytes')
