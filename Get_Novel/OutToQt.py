from PyQt5 import QtWidgets,QtCore
import sys



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
        QtWidgets.qApp.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents | QtCore.QEventLoop.ExcludeSocketNotifiers)
                                            #refresh UI's log box
    def processInfo(self, info):
        self.out_object.log.append(info+'\n')  #print into UI's log box
        self.out_object.log.moveCursor(self.out_object.log.textCursor().End)

    def restoreStd(self):               #Restore stdout and stderr
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

    def __del__(self):
        self.restoreStd()