import os

Current_dir=os.getcwd()
path=Current_dir+'\道君\\'+'第一章 没白来.txt'
if os.path.exists(path):
    print('文件已存在')