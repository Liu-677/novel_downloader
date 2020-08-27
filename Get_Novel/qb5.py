from bs4 import BeautifulSoup
import requests
from Get_Novel import convert
import os
import threading
from queue import Queue
import time



class quanben5:
    def __init__(self):
        self.search_url='https://www.qb5.tw/modules/article/search.php?searchkey='
        self.header={ 'User-Agent':
                          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        self.titleroot = '的搜索结果-全本小说网'
        self.novel_list = []
        self.chapter_list = []
        self.choose_index=5
        self.Current_dir = os.getcwd()
        self.display=True
        self.isall=True

    def Find_Novel(self,novel_name):              #function: find the novel  parameter:novel's name  return:the url of novel
        self.novel_name=novel_name
        url=self.search_url+convert.str_encode(self.novel_name)  #Get the search url
        htmlSource=requests.get(url,headers=self.header)   #Get the html of search url
        soup=BeautifulSoup(htmlSource.text,'lxml')    #Parsing the html
        head=soup.find('head')
        self.novel_list = []                #judge whether the page is a search page
        self.items = []
        if head.title.text!=novel_name+self.titleroot:    #This is the homepage of a novel
            info=soup.find('div',attrs={'id':'bookdetail'}).find('div',attrs={'id':'info'}) #get the information of this novel
            name,author=info.h1.text.split('/ ')     #Novel's name author state link and introduction
            state=info.p.span.next_sibling.text
            self.items.append(name)
            link = head.link['href']
            novel_info = (name, author, '无法获取', state, link)
            self.novel_list.append(novel_info)
        else:                                          # This is search page
            trs=soup.find_all('tr',attrs={'align':False})   #Get information about all novels on this page
            for tr in trs:
                tds=tr.find_all('td')
                novel_info=(tds[0].text,tds[2].text,tds[3].text,tds[5].text,tds[0].find('a')['href'])
                self.items.append(tds[0].text)          #Add all novels' name into the items
                self.novel_list.append(novel_info)      #Add all novels' information into the novel_list
        if self.items == []:
            print('未检测到小说')
        else:
            print('检索完成！')



    def Get_chapter_list(self):
        html=requests.get(self.novel_list[self.choose_index][4],headers=self.header).text
        soup = BeautifulSoup(html, 'lxml')                            #Parsing the html
        self.introduction=soup.find('div',attrs={'id':'intro'}).text
        self.introduction=''.join(self.introduction.split())               #get the novel's introduction
        self.img=soup.find('div',attrs={'class':'img_in'}).img['src']
        chapters=soup.find('dl',attrs={'class':'zjlist'}).find_all('a')     #get the chapter's url and name
        self.chapter_list=[]
        self.start=0
        self.end=0
        num=0
        long=len(chapters)               #Filter useless chapters:there are up to 12 useless chapter in the novel's homepage
        if long<24:                      #if useless chapters less than 12 ,the number of chapters we have gotten must be even
            latest=long/2
        else:
            latest=12
        forget=0
        for chapter in chapters:
            if forget>=latest:
                flag=(chapter.text,self.novel_list[self.choose_index][4]+chapter['href'],str(num+1))
                self.chapter_list.append(flag)      #save the chapters name and url
                num+=1
            forget+=1
        self.chapters_num=num

    def Download_img(self):        #Download the cover of the novel
        self.img_res=requests.get(self.img,headers=self.header)


    def Choose_novel(self,index):
        self.choose_index = index
        self.novel_name = self.novel_list[index][0]
        print('选择小说：' + self.novel_name)
        self.Get_chapter_list()
        self.author = self.novel_list[index][1]
        self.name = self.novel_list[index][0]
        self.wordnum = self.novel_list[index][2]
        self.state = self.novel_list[index][3]
        self.Download_img()



    def get_queue(self):                   #function : put chapters into a queue
        if self.isall:                                    #download all chapters of the  novel
            self.chapter_queue = Queue(self.chapters_num)
            for chapter in self.chapter_list:
                self.chapter_queue.put(chapter)
            return 0
        else:                                            #download part chapters of the  novel by the index of start and end
            if self.start>self.end or self.start<=0 or self.end<=0:   #   invalid index
                return -1
            elif self.end>self.chapters_num or self.start>self.chapters_num:
                return -2
            else:
                self.chapter_queue = Queue(self.end - self.start+1)
                for i in range(self.start-1, self.end):
                    self.chapter_queue.put(self.chapter_list[i])
                return 0


    def threads(self,num):
        CurrentThread_num = len(threading.enumerate())    #Get the total number of current threads
        for i in range(num):                              #Generate the download thread
            i=Consumer(self.chapter_queue,self.novel_name)
            i.start()
        Monitor=threading.Thread(target=self.Monitor_thread,args=(CurrentThread_num,))  #Monitor download threads
        Monitor.start()

    def Monitor_thread(self,last):                              #Monitor download threads: if all download threads finished
        thread_num = len(threading.enumerate())                 #When all download threads are finished,
                                                                # print the download completion message
        print('当前线程数：'+str(thread_num))
        while thread_num-last>1:
            thread_num = len(threading.enumerate())
        print("下载完成")

    def Download_Novel(self):
        index_error=self.get_queue()      #judge the index
        if index_error==-1:
            print('索引非法')
        elif index_error==-2:
            print('索引超出章节范围')
        else:
            print("从第" + str(self.start) + '章到第' + str(self.end) + '章')
            if self.chapter_queue.empty():
                print('队列为空')
                return
            path = self.Current_dir + '\\' + self.novel_name
            print('缓存路径：' + path)
            if os.path.exists(path):      #Create chapter save path
                print('文件夹已存在')
            else:
                os.makedirs(path)
                print('成功创建文件夹：' + path)

            self.threads(10)               #Start download


class Consumer(threading.Thread):
    def __init__(self,chapter_queue,novel_name, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.chapter_queue = chapter_queue
        self.Current_dir = os.getcwd()
        self.novel_name=novel_name
        self.header = {'User-Agent':
                           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    def run(self):
        while True:
            if self.chapter_queue.empty():
                break
            chapter_info= self.chapter_queue.get()
            self.download_chapter(chapter_info)

    def download_chapter(self,chapter_info):    #function:download the chapter
        chapter_url=chapter_info[1]
        html = requests.get(chapter_url, headers=self.header).text
        soup = BeautifulSoup(html, 'lxml')
        contents=soup.find('div',attrs={'id':'readbox'}).find('div',attrs={'id':'content'}).text
        contents=chapter_info[0]+'\n'+'  '+'\n  '.join(contents.split())  #get the chapter's content
        path = self.Current_dir + '\\' + self.novel_name
        chapter_name=path + '\\' + chapter_info[2] + chapter_info[0] + '.txt'  #Generate chapter name and save path
        if os.path.exists(chapter_name):
            print('文件已存在')
        else:
            with open(chapter_name,'w',encoding='utf-8') as f:   #save the chapter
                f.write(contents)
            print('已下载：' + chapter_info[0]+' 时间：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
if __name__== '__main__':
    pass