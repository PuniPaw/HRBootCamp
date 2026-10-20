# BeautifulSoup 객체를 이용한 문서(html, xml) 처리
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

baseurl = "https://www.naver.com"
headers = {"User-Agent": "Mozilla/5.0"}

source = requests.get(baseurl, headers=headers)
print(source, type(source))     # <Response [200]> <class 'requests.models.Response'>
print(source.status_code)       # 200
# print(source.text, type(source.text))
# print(source.content)

conv_data = BeautifulSoup(source.text, 'html.parser')
# print(conv_data, type(conv_data))

links = []
for atag in conv_data.find_all("a"):
    fref = atag.get("href")
    title = atag.get_text(strip=True)

    # href나 텍스트가 없는 태그는 건너뛰기
    if not fref or not title:
        continue

    # 상대경로("/news" 등)를 절대경로로 변환
    fref = urljoin(baseurl, fref)

    links.append({"title": title, "href": fref})
    print(f"{title} -> {fref}")

print("총 링크 수:", len(links))