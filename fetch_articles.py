import urllib.request
import re
from html import unescape
import json

urls = [
    'https://mccc.my/en/mccc-branches/branch-pahang-intro/',
    'https://eastcoast.chinapress.com.my/20210207/%E2%97%A4%E7%9C%8B%E8%A7%86%E9%A2%91%E2%97%A2%E5%8A%A0%E7%B4%A7%E4%B8%8E%E5%8D%8E%E8%A3%94%E9%97%B4%E7%9A%84%E8%81%94%E7%B3%BB-%E6%A2%81%E4%B8%9A%E6%B5%B7%E8%A2%AB%E5%A7%94%E4%BB%BB%E8%8B%B1/',
    'https://eastcoast.chinapress.com.my/?p=102187',
    'https://www.enanyang.my/news/20180121/State/104482',
    'https://eastcoast.sinchew.com.my/news/20210716/eastcoast/3237267',
    'https://www.enanyang.my/news/20170921/State/116746',
    'https://eastcoast.chinapress.com.my/20191229/%E8%B5%9B%E5%A4%AB%E4%B8%81%E9%98%BD%E9%83%BD%E6%8B%89%EF%BC%9A-%E7%A1%AE%E4%BF%9D%E9%80%89%E5%8C%BA%E5%AD%A6%E7%94%9F-%E5%BC%80%E5%AD%A6%E6%97%B6-%E6%9C%89%E8%AF%BE%E6%9C%AC-%E6%A1%8C%E6%A4%85/',
    'https://eastcoast.chinapress.com.my/20211019/%E8%B5%9B%E5%A4%AB%E4%B8%81%EF%BC%9A%E5%9B%BD%E5%AE%B6%E6%9C%AA%E6%9D%A5%E4%B8%BB%E4%BA%BA%E7%BF%81-%E9%9D%92%E5%B0%91%E5%B9%B4%E6%84%8F%E8%A7%81-%E5%BA%94%E8%8E%B7%E9%87%8D%E8%A7%86/',
    'https://eastcoast.chinapress.com.my/20200324/%E6%8D%90%E5%8F%A3%E7%BD%A9%E6%90%93%E6%89%8B%E6%B6%B2%E5%8A%A9%E9%98%B2%E7%96%AB-%E4%BC%81%E4%B8%9A%E8%B5%A0%E5%89%8D%E7%BA%BF%E4%BA%BA%E5%91%98%E7%89%A9%E8%B5%84/',
    'https://www.sinchew.com.my/20190426/%E4%B8%8A%E6%B5%B7%E6%96%87%E5%8C%96%E4%BD%BF%E8%80%85%EF%BC%8E%E5%90%91%E5%85%89%E5%8D%8E%E7%94%9F%E6%8E%A8%E5%B9%BF%E9%98%85%E8%AF%BB/'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

results = []

for i, url in enumerate(urls):
    print(f"Fetching {i+1}/{len(urls)}: {url}")
    item = {'url': url, 'title': '', 'content': '', 'status': 'ok'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            item['title'] = unescape(title_m.group(1).strip()) if title_m else ''
            
            # Remove scripts, styles
            clean = re.sub(r'<(script|style|nav|header|footer)[^>]*>.*?</\1>', '', html, flags=re.I|re.S)
            text = re.sub(r'<[^>]+>', '\n', clean)
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            full_text = '\n'.join(lines)
            item['content'] = full_text
    except Exception as e:
        item['status'] = f'error: {str(e)}'
        print(f"Error fetching {url}: {e}")
    results.append(item)

with open('scraped_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to scraped_results.json successfully!")
