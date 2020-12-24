from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
import functools
from news_api import NewsAPI


class News_Widget:
    
    news_data = None
    
    # User settings
    scroll_speed = 2
    num_of_news_to_show = 20 # number of top news to show
    refresh_news_delay = 360000 # 30mins
    keywords = {'arrested ':'red', 'riot':'yellow'} # Keywords to spot and corresponding color
    

    
    def __init__(self, master): 
    
        self.wid_frame = QtWidgets.QWidget(master, objectName = "news_widget_frame")
        self.wid_frame.setGeometry(50,int(master.s_height*0.9),int(master.s_width*0.92),50)
        self.wid_frame.setStyleSheet("QWidget#"+self.wid_frame.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(255,255,255, 5);"
                                "}")
        self.wid_frame.mouseMoveEvent = functools.partial(master.movementHandler, source_object=self.wid_frame)

        self.news_label = QtWidgets.QLabel(self.wid_frame, objectName='news_label', text='Lorem ip') 
        self.news_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.news_label.setGeometry(20, 0, self.wid_frame.width(), 50) 
        self.news_label.setFont(QtGui.QFont('Roboto Light', 20)) 
        self.news_label.setStyleSheet("QLabel#"+self.news_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "animation:"
                                "}")

        self.news_label2 = QtWidgets.QLabel(self.wid_frame, objectName='news_label2', text='Lorem ip') 
        self.news_label2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.news_label2.setGeometry(self.wid_frame.width(), 0, self.wid_frame.width(), 50) 
        self.news_label2.setFont(QtGui.QFont('Roboto Light', 20)) 
        self.news_label2.setStyleSheet("QLabel#"+self.news_label2.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")

        self.n_api = NewsAPI(master)
        self.news_data = self.n_api.get_news(self.num_of_news_to_show, self.keywords)

        self.fm = self.news_label.fontMetrics()

        # To remove HTML tags to get an accurate width
        tmp_news_data = self.news_data.replace('&nbsp;',' ').replace("<font color=\"red\">","").replace("</font>","")
        
        # Need to redo this whenever get new RSS feed
        self.calc_width = self.fm.averageCharWidth()*len(tmp_news_data)
        self.news_label.setGeometry(self.wid_frame.width(),0, self.calc_width, 50)
        self.news_label.setText(self.news_data)
        self.news_label2.setGeometry(self.news_label.x()+ self.news_label.width() +120 ,0, self.calc_width, 50)
        self.news_label2.setText(self.news_data)

    
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.anim())
        self.timer.start(10)

        self.grab_timer = QtCore.QTimer()
        self.grab_timer.timeout.connect(lambda: self.grab_news())
        self.grab_timer.start(self.refresh_news_delay)

    def grab_news(self):
        self.news_data = self.n_api.get_news(self.num_of_news_to_show, self.keywords)
        self.calc_width = self.fm.averageCharWidth()*len(self.news_data)
        

    def anim(self):
        self.news_label.setGeometry(self.news_label.x()-self.scroll_speed,self.news_label.y(), self.news_label.width(), self.news_label.height())
        self.news_label2.setGeometry(self.news_label2.x()-self.scroll_speed,self.news_label2.y(), self.news_label2.width(), self.news_label2.height())

        if(self.news_label.x() < (self.news_label.width())*-1):
            self.news_label.setText(self.news_data) # to show latest news in the next scroll
            self.news_label.setGeometry(self.news_label2.x()+ self.news_label2.width() +120, 0, self.calc_width, 50)
        
        if(self.news_label2.x() < (self.news_label2.width())*-1):
            self.news_label2.setText(self.news_data) # to show latest news in the next scroll
            self.news_label2.setGeometry(self.news_label.x()+ self.news_label.width() +120, 0, self.calc_width, 50)
        
            
        




 