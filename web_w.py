from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore, QtNetwork
import functools

# TODO: change to class style..


def UiComponents(self, url_): 

    wid_frame = QtWidgets.QWidget(self, objectName = "web_widget_frame")
    wid_frame.setGeometry(600,300,600,600)
    wid_frame.setStyleSheet("QWidget#"+wid_frame.objectName()+""       # To ensure stylesheet only applies to parent
                            "{"
                            #"background-color: rgba(135,206,250, 180);"
                            "background-color: rgba(1,1,1, 255);"
                            "border : 2px solid white;"
                            "border-radius: 12px;"
                            "}")
    wid_frame.mouseMoveEvent = functools.partial(self.movementHandler, source_object=wid_frame)
   
    
    

    closeButton = QtWidgets.QPushButton(wid_frame, objectName = 'clsButton')
    closeButton.setGeometry(20,540,wid_frame.width()-40,40)
    closeButton.setFont(QtGui.QFont('Roboto', 14)) 
    closeButton.setText("CLOSE")
    closeButton.setStyleSheet("QWidget#"+closeButton.objectName()+""       # To ensure stylesheet only applies to parent
                            "{"
                            "background-color: red;"
                            "border-radius: 15px;"
                            "color: white;"
                            "}") 
    
    web = QtWebEngineWidgets.QWebEngineView(wid_frame)
    web.setGeometry(20, 50, wid_frame.width()-40, int(wid_frame.height()*0.80)) 
    web.setStyleSheet(     
                            "{"
                            "background:transparent;"
                          
                            "}") 
    web.load(QtCore.QUrl(url_))
    
    web.show()
    closeButton.clicked.connect(lambda: closeApp(web, wid_frame))
    
    wid_frame.show()
    
    return wid_frame
    
def closeApp(web, wid_frame):
    web.close()
    wid_frame.close()