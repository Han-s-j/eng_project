import os.path
from os import write

import openpyxl
import pip
from bs4 import BeautifulSoup
import requests
import csv
import urllib.request as req
from selenium import webdriver
import time
import pandas as pd
import openpyxl

url = 'https://www.oxfordlearnersdictionaries.com/definition/english/star_1?q=star'
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

div = soup.select_one('#star_1')

#print(div)
# 'star_1' div 안에 있는 모든 <ol> 요소를 찾음
ols = div.find_all('ol')

# 리스트로 예문을 저장
examples_list = []

#print(ols)
# 각 <ol> 안에 있는 <ul> 요소들 중에서 예문을 포함하는 <ul>만 찾아 처리
for ol in ols:
    uls = ol.find_all('ul', class_='examples')
    for ul in uls:
        # <span class"x"> 안의 텍스트를 추출
        examples = ul.find_all('span', class_='x')
        for examples in examples:
            examples_list.append(examples.get_text())  # 예문 텍스트를 리스트에 추가

#print(examples.get_text())   # 예문 텍스트만 출력

# pandas DataFrame을 사용하여 예문을 엑셀로 저장
df = pd.DataFrame(examples_list, columns=["Examples"])

# 예문을 엑셀 파일로 저장
df.to_excel("examples.xlsx", index=False)

print("Examples saved to 'examples.xlsx'")