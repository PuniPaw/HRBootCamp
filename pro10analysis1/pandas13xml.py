# BeautifulSoup 객체로 XML 문서 처리
from bs4 import BeautifulSoup

with open("pandas9my.xml", mode='r', encoding='utf-8') as f:
    xmlfile = f.read()
    print(xmlfile, type(xmlfile))

soup = BeautifulSoup(xmlfile, "lxml")
print(type(soup))

itemTag = soup.find_all('item')
print(itemTag[1])
print(itemTag[1].find('name')['id'])

print('---')
for i in itemTag:
    nameTag = i.find_all('name')
    for j in nameTag:
        print('id: ', j['id'] + ' name: ', j.string)
        tel = i.find('tel')
        print('tel: ', tel.string)

    for j in i.find_all('exam'):
        print('kor: ' + j['kor'] + ', eng: ' + j['eng'])
    print()

print('\n\n 서울시 제공 도서관 xml 문서 정보 읽기')
import urllib.request as req
import pandas as pd

url = "http://openapi.seoul.go.kr:8088/sample/xml/SeoulLibraryTimeInfo/1/5/"
plainText = req.urlopen(url).read().decode()
# print(plainText)

xmlObj = BeautifulSoup(plainText, 'xml')    # lxml은 문서를 html로 해석하기 때문에 대소문자를 구분하지 않음 -> lbrry_name으로 변환되어 데이터를 찾을 수 없다
libData = xmlObj.select('row')
# print(libData)
rows = []
for data in libData:
    name = data.find('LBRRY_NAME')
    addr = data.find('ADRES')
    print('도서관명: ', name)
    print('주소: ', addr)
    print()
    rows.append({'도서관명':name,'주소':addr})

df = pd.DataFrame(rows)
print(df)
print('건수: ', len(df))