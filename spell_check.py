from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

fp = open("test1.txt", 'r', encoding="utf-8")
text = fp.read()
fp.close()


ready_list = []
while (len(text) > 500):
    temp_str = text[:500] #0부터 500까지 저장
    last_space = temp_str.rfind(' ') # 500자 전에 가장 가까운 공백찾아 저장
    temp_str = text[0:last_space] #문자열 범위 재조정
    ready_list.append(temp_str) #재조정된 문자열을 리스트에 추가

    text = text[last_space:]  #최초 텍스트 중 추가된 문자열 제거

ready_list.append(text) #500글자 이하 나머지 리스트에 추가


dv = webdriver.Chrome('C:\Python\chromedriver.exe')
dv.get("http://www.naver.com")

elem = dv.find_element_by_name("query")
elem.send_keys("맞춤법 검사기")
elem.send_keys(Keys.RETURN)

time.sleep(1)
textarea = dv.find_element_by_class_name("txt_gray")

new_str = ''
for ready in ready_list:
    
    textarea.send_keys(Keys.CONTROL,"a")
    textarea.send_keys(ready)

    elem = dv.find_element_by_class_name("btn_check")
    elem.click()

    time.sleep(1)

    soup = BeautifulSoup(dv.page_source, 'html.parser')
    st = soup.select("p._result_text.stand_txt")[0].text
    new_str += st.replace('. ', '.\n')

fp = open("result.txt", 'w', encoding='utf-8')
fp.write(new_str)
fp.close()

