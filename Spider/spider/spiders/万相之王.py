import lxml
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import base64
url = 'https://www.beqege.com/61297/817291.html'

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 '
#                   'Safari/537.36'
# }
# params = {
# }
# response = requests.get(url, headers=headers)
# print(response)
# html = lxml.etree.HTML(response.text)
# print(response.text)
options = Options()
options.headless = True
browser = webdriver.Chrome(options)
url_pools = [f'https://www.beqege.com/61297/81729{i}.html' for i in range(1, 10)]
for url in url_pools:
    browser.get(url)
    title = browser.find_element(By.XPATH, '//div[@class="bookname"]/h1').text
    contents = browser.find_element(By.XPATH, '//div[@id="content"]').text
    txt_name = f'md/万相之王/{title}.txt'
    if not os.path.exists(txt_name):
        os.makedirs(os.path.dirname(txt_name), exist_ok=True)
        with open(txt_name, 'w', encoding='utf-8') as f:
            content_with_indentation = '\n\n'.join(['    ' + p for p in contents.split('\n\n')])
            f.write(content_with_indentation)
            f.write('\n')
    else:
        print('文件已存在')
browser.close()

