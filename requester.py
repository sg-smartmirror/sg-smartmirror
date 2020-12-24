
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest,QNetworkAccessManager
import sys
      
  
class RequestHandler:

    request_queue = []

    def __init__(self, master, API_key=None):    

        self.master = master
        
        #self.doRequest()
        
    @QtCore.pyqtSlot('QNetworkRequest')
    def doRequest(self, callback_, base_url, headers = None): 
        print('requesting from ',base_url)
        url = base_url
        req = QNetworkRequest(QtCore.QUrl(url))
        
        if headers != None:
            for k,v in headers.items():
                key = QtCore.QByteArray()
                val = QtCore.QByteArray()
                key.append(str(k))
                val.append(str(v))
                req.setRawHeader(key,val)
        
        self.master.nam = QNetworkAccessManager(self.master)
        self.master.nam.finished.connect(callback_)
        self.master.nam.get(req) 
       