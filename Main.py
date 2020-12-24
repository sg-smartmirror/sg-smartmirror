
#from framegui import GUI
#from webtest import start_web

# importing libraries 
import os
import sys 
from PyQt5 import QtCore, QtNetwork, QtGui, QtWidgets, QtWebEngineWidgets
from screeninfo import get_monitors
import functools
from weather_w import Weather_Widget
from my_clock_w import Clock_Widget
from lta_w import Transport_Widget
from news_w import News_Widget
from app_w import App_Widget







class Window(QtWidgets.QMainWindow): 

    # For widget movements
    homeAction = None

    oldPos = QtCore.QPoint()

    def __init__(self): 
        super().__init__() 

        # Get screen resolution
        self.s_width = 0
        self.s_height = 0

        for m in get_monitors():
            self.s_width = int(m.width)
            self.s_height = int(m.height)
  
        # setting background
        self.setStyleSheet("background-color: black;") 
  
        # setting geometry 
        self.setGeometry(0, 0, self.s_width, self.s_height) 

        # for escape key
        QtWidgets.QShortcut(
            QtGui.QKeySequence("Escape"), self, activated=self.on_Escape
        )


        # widgets
        self.ww = Weather_Widget(self)
        self.cw = Clock_Widget(self)
        self.tw = Transport_Widget(self)
        self.nw = News_Widget(self)
        self.aw = App_Widget(self)


        # for full screen
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)# | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
      
        # showing all the widgets 
        self.showMaximized()  
        
    
    @QtCore.pyqtSlot()
    def on_Escape(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def movementHandler(self, event, source_object=None):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        source_object.move(source_object.x() + delta.x(), source_object.y() + delta.y())
        self.oldPos = event.globalPos()

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()
        #print(evt.globalPos())

   

    def font_init(self):
        for subdir, dirs, files in os.walk('fonts'):
            for file in files:
                #print os.path.join(subdir, file)
                filepath = subdir + os.sep + file
                if filepath.endswith(".ttf"):
                    font_ = filepath.split('\\')
                    font_name = font_[len(font_)-1][:-4].replace("-"," ")
                    #print (font_name)
                    dir_ = QtCore.QDir(font_name)
                    _id = QtGui.QFontDatabase.addApplicationFont(filepath)
                    #print(QtGui.QFontDatabase.applicationFontFamilies(_id))


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv) 
    window = Window() 
    window.font_init()
    sys.exit(App.exec()) 