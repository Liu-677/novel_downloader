



 # 小说下载器V1.0



## 小说获取部分

​		小说来源我选择的是**全本小说网**，本来想的是多选择几个小说源，不过有点麻烦，就留到以后在添加吧。

### 1.小说列表获取

![image-20200827175207816](readme.assets/image-20200827175207816.png)



![image-20200827175317809](readme.assets\image-20200827175317809.png)		这个网站要找到想要的小说只能通过图中的搜索栏，通过观察，搜索结果页的网址构成是有规律的：

'https://www.qb5.tw/modules/article/search.php?searchkey='+编码后的关键字，为了将其编码，编写以下函数：

```python
def str_encode(str):
    return urllib.parse.quote(str.encode('gb2312'))
```

​		对输入字符串先进行gb2312编码，再进行urlencode编码。得到了正确的网址，就能开始爬取小说列表了。





```python
def Find_Novel(self,novel_name):              #function: find the novel  parameter:novel's name  return:the url of novel
    self.novel_name=novel_name
    url=self.search_url+convert.str_encode(self.novel_name)  #Get the search url
    htmlSource=requests.get(url,headers=self.header)   #Get the html of search url
    soup=BeautifulSoup(htmlSource.text,'lxml')    #Parsing the html
    head=soup.find('head')
    self.novel_list = []                #judge whether the page is a search page
    self.items = []
    if head.title.text!=novel_name+self.titleroot:    #This is the homepage of a novel
        info=soup.find('div',attrs={'id':'bookdetail'}).find('div',attrs={'id':'info'}) 
        										#get the information of this novel
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
```

​		此函数用于获取搜索页的说有小说，并将其储存到列表中，便于之后的UI调用，特别的是，当搜索的关键字只能检索到一本小说的时候，网站会自动跳转到该小说的主页。对此，我使用了一个if来判断。





### 2.小说章节列表获取

```python
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
    long=len(chapters)  
                     #Filter useless chapters:there are up to 12 useless chapter in the novel's homepage
    if long<24:      #if useless chapters less than 12 ,the number of chapters we have gotten must be even
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
```



![image-20200827182950449](readme.assets\image-20200827182950449.png)

​		每本小说都如图，正文开始前都有最新章节列表，这对于我们来说是干扰项，在获取章节列表时，需要过滤这几章，不难发现，最新列表最多有12章，当总章节大于24章是，最新列表有十二章，我们去掉获取的章节中的前十二章就可以了，当总章节小于24时，相当于小说的每一章在正文列表和最新章节列表里各出现了一遍，因此，总章节数一定是偶数，因此，直接去掉总章节的前一半就好了。

### 3.小说下载

​		为了便于下载，我将小说分章下载，这样便于下载是使用多线程。

```python
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
        chapter_name=path + '\\' + chapter_info[2] + chapter_info[0] + '.txt'  
        											#Generate chapter name and save path
        if os.path.exists(chapter_name):
            print('文件已存在')
        else:
            with open(chapter_name,'w',encoding='utf-8') as f:   #save the chapter
                f.write(contents)
            print('已下载：' + chapter_info[0]+' 时间：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
```

​		将章节下载函数重写进threading类，便于多线程的开启，为了防止线程重复访问相同章节，我将章节信息全部放入队列中，相当于给资源加了锁，只能访问一次。

```python
def get_queue(self):                   #function : put chapters into a queue
    if self.isall:                     #download all chapters of the  novel
        self.chapter_queue = Queue(self.chapters_num)
        for chapter in self.chapter_list:
            self.chapter_queue.put(chapter)
        return 0
    else:                              #download part chapters of the  novel by the index of start and end
        if self.start>self.end or self.start<=0 or self.end<=0:   #   invalid index
            return -1
        elif self.end>self.chapters_num or self.start>self.chapters_num:
            return -2
        else:
            self.chapter_queue = Queue(self.end - self.start+1)
            for i in range(self.start-1, self.end):
                self.chapter_queue.put(self.chapter_list[i])
            return 0
        
```

​		此函数用于创建队列，根据输入的索引，若索引错误，则取消下载，并返回错误信息，若正确，则根据索引范围，将章节信息加入队列。

```python
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
```

​		下载前，先创建保存章节的文件夹，之后，由于已经将章节下载函数重构进了Threading类Consumer里面，因此下载时只需要创建若干个Consumer对象，就能在开启线程的时候启动下载，并在下载完成后自动结束线程，之后创建一个线程用于监视下载线程，以便于获取下载进度。

## 用户界面

![image-20200827190712655](readme.assets\image-20200827190712655.png)

​		该界面使用pyqt designer创建，然后使用pyuic生成python代码。信息的交互由按钮和列表的点击事件触发，点击事件的触发主要是通过以下函数。

### 1.搜索按钮的点击

```python
def Serarch_clicked(ui,download):
    ui.novel_list.clear()
    t4 = threading.Thread(target=Search_clicked_thread, args=(ui, download,))
    t4.start()
    
    
def Search_clicked_thread(ui,download):
    novel_name = ui.search_input.text()
    download.Find_Novel(novel_name)
    ui.novel_list.addItems(download.items)
```

​		为了使得界面流畅，各个事件单独使用一个线程来运行，当点击搜索按钮时，会触发Serarch_clicked()函数，此时会调用之前编写的Find_Novel()函数,根据搜索框中的关键字进行检索。得到检索内容后，将会把检索到的小说名称显示到UI界面中小说列表框里。



### 2.小说列表的点击

```python
def Get_novel(ui,download):   #get all imformation of the choosed novel
    download.Choose_novel(ui.novel_list.currentIndex().row())
```

​		此函数通过调用函数Choose_novel()得到选中的小说的各种信息，以便于用于显示。



```python
def Show_info(ui,download):   #print the information into the UI
    info='书名：' + download.name+'\n'+'作者：' + download.author+'\n'+'字数：' + download.wordnum+'\n'+'状态：' +download.state+'\n'+'章数：' + str(download.chapters_num) + '章'+'\n'+'简介：' + download.introduction
    ui.novel_info.append(info)

def Show_img(ui,download):    #print the novel's cover into the UI
    photo = QPixmap()
    photo.loadFromData(download.img_res.content)
    ui.novel_img.setPixmap(photo)

def Show_chapterlist(ui,download):    #print the novel's chapters name into the UI
    for chapter in download.chapter_list:
        ui.chapter_list.addItem(chapter[0])
```

​		以上三个函数用于打印选中小说的封面、简介和章节列表。

```python
def Novel_clicked_thread(ui,download):
    Get_novel(ui, download)
    t1=threading.Thread(target=Show_info,args=(ui, download,))
    t1.start()
    t2 = threading.Thread(target=Show_chapterlist, args=(ui, download,))
    t2.start()
    t3 = threading.Thread(target=Show_img, args=(ui, download,))
    t3.start()
```

​		当小说列表里的某一行被点击时，此函数会被调用，此函数主要用于产生多个线程来打印信息到UI界面中。值得注意的是，函数Get_novel()必须要先于其他几个函数完成，因此其他三个函数所用到的信息都由函数Get_novel()生成，因此，函数Get_novel()不能放入与其他三个函数并行的线程中，且必须先于其他函数完成，因此，将Get_novel()放入主线程，在此函数结束时，在创建用于信息展示的线程。

### 3.下载按钮的点击

​		下载分为全本下载和部分章节下载，当选择部分下载时，须在文本框中输入下载的章节索引。

```python
def downloadAll_clicked(download):
    print('全本下载')
    download.isall = True
    download.Download_Novel()

def downPart_clicked(ui,download):
    download.isall=False
    download.start=ui.start.value()
    download.end=ui.end.value()
    download.Download_Novel()
```

​		以上两个函数在分别在点击全本下载按钮和下载按钮是调用，因为下载时已经启用了其他线程，因此，这两个函数不会占用主线程太久。两个函数都是通过调用Download_Novel()函数启动下载，不同点在于传入的参数不同，部分下载还需传入起始和终止索引。

### 4.过程信息打印

​		为了在UI界面中实时显示进程 信息，我将函数print()的输出重定向到了UI界面上。

```python
class myStdout():
    def __init__(self,ui):
        self.stdoutbak = sys.stdout #Backup the stdout and stderr
        self.stderrbak = sys.stderr
        sys.stdout = self            #Redirect stdout and stderr to the current object
        sys.stderr = self
        self.out_object=ui

    def write(self, info):
        str = info.rstrip("\r\n")
        if len(str): self.processInfo(str)  # Process output information
        QtWidgets.qApp.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents | 														QtCore.QEventLoop.ExcludeSocketNotifiers)
                                            #refresh UI's log box
    def processInfo(self, info):
        self.out_object.log.append(info+'\n')  #print into UI's log box
        self.out_object.log.moveCursor(self.out_object.log.textCursor().End)

    def restoreStd(self):               #Restore stdout and stderr
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

    def __del__(self):
        self.restoreStd()
```



### 5.主函数

```python
if __name__ == '__main__':
    download = quanben5()   #Create novel download objects
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = novel.Ui_MainWindow()    #Create user interface
    out=myStdout(ui)       #Enable Redirect output
    ui.setupUi(MainWindow) #Initialize the user interface
    MainWindow.show()
    ui.search.clicked.connect(partial(Serarch_clicked, ui,download))        #Search button Slot function
    ui.novel_list.itemClicked.connect(partial(Novel_clicked, ui,download))  #Novel list Slot function
    ui.downloadAll_btn.clicked.connect(partial(downloadAll_clicked, download)) #Download Slot function
    ui.downPart_btn.clicked.connect(partial(downPart_clicked, ui,download))
    sys.exit(app.exec_())  #keep the window alive
```

​		主函数主要用于创建初始化下载对象和用户界面，使能输出重定向并将各个信号和与之对应的槽函数连接。





## 2020.08.28更新

1.修复了当搜索结果为1时，获取到的小说昵称后有一空格导致无法创建文件及目录的问题：

```python
name=name.split()[0]
```

​		在函数Find_Novel()里加入这一行代码，去掉空格

2.加入章节合并功能

```python
def Merged_chapters(self):
    filenames = os.listdir(self.chapters_path)
    regular = r'\d+'
    filenames.sort(key=lambda x: int(re.findall(regular, x)[0]))
    with open(self.save_path+self.novel_name+'.txt', 'w', encoding='utf-8') as novel:
        for filename in filenames:
            filepath = self.chapters_path +'\\'+ filename
            for line in open(filepath, encoding='utf-8'):
                novel.writelines(line)
            novel.write('\n')
            print('已合并：' + filename)
```

​		遍历存储章节的文件夹，将里面的文件全部写入新的文件，为了按正确的章节顺序写入文件，在读写前先进行排序，排序按章节标题最前面的数字，该数字的获取使用正则表达式



## 开发过程中有参考性的文档

### 1.多线程：

* https://zhuanlan.zhihu.com/p/62988456  
* https://www.jianshu.com/p/c7c2fb69137b (最有价值)
* https://blog.csdn.net/aojiancc2/article/details/83781140?utm_medium=distribute.pc_relevant.none-task-blog-title-1&spm=1001.2101.3001.4242

### 2.编码：

* https://blog.csdn.net/qq_38607035/article/details/82594822

### 3.pyqt使用：

* https://www.tutorialspoint.com/pyqt/pyqt_qlistwidget.htm （list weight 文档）

### 4.print重定向到pyqt：

* https://blog.csdn.net/LaoYuanPython/article/details/105316856

### 5.beautifulsoup：

* https://blog.csdn.net/xudailong_blog/article/details/80398258?utm_source=blogxgwz6 (.next_sibling的使用)

### 6.禁止窗口拉伸：

* https://www.cnblogs.com/Javauser/p/8951863.html

### 7.文件合并

* 文件排序 https://www.cnblogs.com/chester-cs/p/12252358.html
* 文件合并 https://blog.csdn.net/qq_24326765/article/details/82556085
