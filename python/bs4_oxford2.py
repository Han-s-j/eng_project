import os.path
from os import write
from bs4 import BeautifulSoup
import requests
import csv
import urllib.request as req
from selenium import webdriver
import time
# csv_filename = "sentence.csv"
url = 'https://www.oxfordlearnersdictionaries.com/definition/english/star_1?q=star'
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
time.sleep(1)
csv_filename = "eng3.csv"
# res = requests.get(url)
# print(res.status_code)
# soup = BeautifulSoup(res.content, 'html.parser')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()


# div = soup.select_one('#star_1')  # 특정 id 선택자
# 예시에서는 soup 전체에서 <ul> 내 <li> 태그를 추출
ols = soup.find_all('ul', class_='examples', encoding='utf-8')  # class가 'examples'인 ul 태그만 찾기
with open(csv_filename, mode='w', newline="") as file:
    writer = csv.writer(file, delimiter='|')
    for ol in ols:
        lis = ol.find_all('li')  # 각 <ul> 내의 <li> 태그 찾기
        for li in lis:
            # <li> 태그 내의 텍스트만 추출
            example_sentence = li.get_text(strip=True)
            print(example_sentence)  # 텍스트 출력
            writer.writerow([example_sentence])
print(f'csv 파일 {csv_filename} 저장 완료')