import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import  QPixmap
from Get_Novel.qb5 import quanben5
from UI import novel
from functools import partial
import threading
from Get_Novel.OutToQt import myStdout

def Get_novel(ui,download):   #get all imformation of the choosed novel
    download.Choose_novel(ui.novel_list.currentIndex().row())

def Show_info(ui,download):   #print the information into the UI
    info='书名：' + download.name+'\n'+'作者：' + download.author+'\n'+'字数：' + download.wordnum+'\n'+'状态：' +download.state+'\n'+ \
         '章数：' + str(download.chapters_num) + '章'+'\n'+'简介：' + download.introduction
    ui.novel_info.append(info)

def Show_img(ui,download):    #print the novel's cover into the UI
    photo = QPixmap()
    photo.loadFromData(download.img_res.content)
    ui.novel_img.setPixmap(photo)

def Show_chapterlist(ui,download):    #print the novel's chapters name into the UI
    for chapter in download.chapter_list:
        ui.chapter_list.addItem(chapter[0])

def Novel_clicked_thread(ui,download):
    Get_novel(ui, download)
    t1=threading.Thread(target=Show_info,args=(ui, download,))
    t1.start()
    t2 = threading.Thread(target=Show_chapterlist, args=(ui, download,))
    t2.start()
    t3 = threading.Thread(target=Show_img, args=(ui, download,))
    t3.start()

def Search_clicked_thread(ui,download):
    novel_name = ui.search_input.text()
    download.Find_Novel(novel_name)
    ui.novel_list.addItems(download.items)


def Serarch_clicked(ui,download):
    ui.novel_list.clear()
    t4 = threading.Thread(target=Search_clicked_thread, args=(ui, download,))
    t4.start()


def Novel_clicked(ui,download):
    ui.novel_img.clear()
    ui.novel_info.clear()
    ui.chapter_list.clear()
    Novel_tread=threading.Thread(target=Novel_clicked_thread,args=(ui,download,))
    Novel_tread.start()


def downloadAll_clicked(download):
    print('全本下载')
    download.isall = True
    download.Download_Novel()

def downPart_clicked(ui,download):
    download.isall=False
    download.start=ui.start.value()
    download.end=ui.end.value()
    download.Download_Novel()


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