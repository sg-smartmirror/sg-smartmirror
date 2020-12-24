from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
import functools


class Clock_Widget:
    
    def __init__(self, master): 
    
        wid_frame = QtWidgets.QWidget(master, objectName = "clock_widget_frame")
        wid_frame.setGeometry(1500,10,350,140)
        wid_frame.setStyleSheet("QWidget#"+wid_frame.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(135,206,250, 180);"
                                "border : 2px solid white;"
                                "border-radius: 12px;"
                                "}")
        wid_frame.mouseMoveEvent = functools.partial(master.movementHandler, source_object=wid_frame)

       

        time_label = QtWidgets.QLabel(wid_frame, objectName='time_label', text='15:33') 
        time_label.setAlignment(QtCore.Qt.AlignCenter)
        time_label.setGeometry(0, wid_frame.y(), wid_frame.width(), 80) 
        time_label.setFont(QtGui.QFont('Roboto Thin', 64)) 
        time_label.setStyleSheet("QLabel#"+time_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        daydate_label = QtWidgets.QLabel(wid_frame, objectName='daydate_label', text='Thursday, December 17') 
        daydate_label.setAlignment(QtCore.Qt.AlignCenter)
        daydate_label.setGeometry(0, time_label.y()+time_label.height()-25, wid_frame.width(), 80) 
        daydate_label.setFont(QtGui.QFont('Roboto Light', 14)) 
        daydate_label.setStyleSheet("QLabel#"+daydate_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        self.updateTime(time_label, daydate_label)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.updateTime(time_label, daydate_label))
        self.timer.start(60000)



    def updateTime(self, time_label, daydate_label):
        time = QtCore.QDateTime.currentDateTime().toString('hh:mm')
        now = QtCore.QDate.currentDate()
        daydate = now.toString('dddd, MMMM d')
        #print("Updated!")
        #print(time)
        #print(daydate)
        time_label.setText(time)
        daydate_label.setText(daydate)

   