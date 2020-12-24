from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore, QtNetwork
import functools
import web_w
import sys

# Change into class style
class App_Widget():
    def __init__(self, master):

        wid_frame = QtWidgets.QWidget(master, objectName = "app_widget_frame")
        wid_frame.setGeometry(1760,570,90,375)
        wid_frame.setStyleSheet("QWidget#"+wid_frame.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(135,206,250, 180);"
                                "border : 2px solid white;"
                                "border-radius: 12px;"
                                "}")
        wid_frame.mouseMoveEvent = functools.partial(master.movementHandler, source_object=wid_frame)

        app_name = ['instagram','youtube','reddit','cna']
        app_icons = ['instagram','youtube','reddit','cna']
        app_urls = ['https://www.instagram.com','https://www.youtube.com/','https://www.reddit.com','https://www.channelnewsasia.com']
        
        previous_offset = 30
        for i in range(0, len(app_name)):
            app = self.create_app_icons(master, wid_frame, app_name[i], previous_offset, "./assets/app_icons/"+app_icons[i]+".png", app_urls[i])
            previous_offset = app.y()+app.height() + 20
        
        
    
    def create_app_icons(self, main_master ,master, objName, y, image_path, url_):
        app_button = QtWidgets.QPushButton(master, objectName = objName)
        app_button.setGeometry(15,y,64,64)
        app_button.setIconSize(QtCore.QSize(64,64))
        app_button.setIcon(QtGui.QIcon(image_path))
        app_button.clicked.connect(lambda: self.openApp(main_master, url_))
        app_button.setStyleSheet("QWidget#"+app_button.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(0,0,0,0);"
                                "}") 
        return app_button

    def openApp(self, main_master, url):  
            web_w.UiComponents(main_master, url)




    


  


