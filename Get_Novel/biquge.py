from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from gzip import GzipFile
import requests
import io
import urllib
import zlib
root='http://www.xbiquge.la/'
header={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
def Find_Novel(novel_name):              #function: find the novel  parameter:novel's name  return:the url of novel
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver=webdriver.Chrome(chrome_options=chrome_options)
    driver.get(root)
    driver.find_element_by_name('searchkey').send_keys(novel_name)
    driver.find_element_by_xpath("//button[@id='sss' and @type='submit']").click()
    pageSource = driver.page_source
    driver.quit()
    soup=BeautifulSoup(pageSource,'lxml')
    trs=soup.find_all('tr',attrs={'align':False})
    novel_list=[]
    for tr in trs:
        tds=tr.find_all('td',attrs={'class':'even'})
        novel_info=(tds[0].text,tds[1].text,tds[0].find('a')['href'])
        novel_list.append(novel_info)
    return novel_list

def loadData(url):
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip,deflate')
    response = urllib.request.urlopen(request)
    content = response.read()
    encoding = response.info().get('Content-Encoding')
    if encoding == 'gzip':
        content = gzip(content)
    elif encoding == 'deflate':
        content = deflate(content)
    return content.decode('utf-8')
def gzip(data):
    buf = io.BytesIO(data)
    f = GzipFile(fileobj=buf)
    return f.read()

def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def get_chapter():
    html = requests.get('https://www.qb5.tw/book_50909/16471552.html', headers=header).text
    soup = BeautifulSoup(html, 'lxml')
    contents=soup.find('div',attrs={'id':'readbox'}).find('div',attrs={'id':'content'})
    print(contents.text)
def Get_Novel():
    html=requests.get('https://www.qb5.tw/book_50909/',headers=header).text
    # html=loadData('http://www.xbiquge.la/15/15003/')
    soup = BeautifulSoup(html, 'lxml')
    chapter_list=soup.find('dl',attrs={'class':'zjlist'}).find_all('dd')
    state=False
    for chapter in chapter_list:
        if chapter.text[0]=='第' and chapter.text[1]=='一' and chapter.text[2]=='章':
            state=True
        if state:
            print(chapter.text,chapter.a['href'])
if __name__== '__main__':
    Get_Novel()
    # get_chapter()