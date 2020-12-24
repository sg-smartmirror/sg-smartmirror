
import functools

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from lta_api import TransportAPI

class Transport_Widget():

    # User data
    bus_stop_code = '70269'
    busses = ['8','22','43','70','76','158']
    icon_asset_path = './assets/traffic_icons/'

    def __init__(self, master): 
        
        self.widget_width = 350
        self.master = master
        self.t_api = TransportAPI(master, self.updateLabels)

        

        self.wid = QtWidgets.QWidget(master, objectName = "traffic_widget")
        self.wid.setGeometry(1500,165,350,75+len(self.busses)*50)
        self.wid.setStyleSheet("QWidget#"+self.wid.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                               # "background-color: rgba(135,108,108, 255);
                                "background-color: rgba(0,0,0, 255);"
                                "border : 2px solid white;"
                                "border-radius: 12px;"
                                "}")
        
        # Glow effect
        self.effect =  QtWidgets.QGraphicsDropShadowEffect(self.wid)
        self.effect.setOffset(0,-2)
        self.effect.setBlurRadius(70)
        self.wid.setGraphicsEffect(self.effect)

        self.wid.mouseMoveEvent = functools.partial(master.movementHandler, source_object=self.wid)

        # Top panel
        self.location_logo = self.createImageLogo(self.wid, 'location_logo', './assets/traffic_icons/bus-stop.png', 10, 15, 32,0)
        self.location_label = QtWidgets.QLabel(self.wid, objectName='location_label', text='Bus stop name') 
        self.location_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.location_label.setGeometry(self.location_logo.x()+45, self.location_logo.y()-2, 340, 35) 
        self.location_label.setFont(QtGui.QFont('Roboto Medium', 14)) 
        self.location_label.setStyleSheet("QLabel#"+self.location_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        self.vertical_line = QtWidgets.QLabel(self.wid, objectName='vertical_line', text='_'*43) 
        self.vertical_line.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.vertical_line.setGeometry(self.location_logo.x()+5, self.location_label.y()+25, 340, 35) 
        self.vertical_line.setFont(QtGui.QFont('Roboto Black', 12)) 
        self.vertical_line.setStyleSheet("QLabel#"+self.vertical_line.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        self.bus_widget = {}
        previous_bus = None
        for i in self.busses:
            bus_icon1 = self.icon_asset_path+'grey_bus.png'
            bus_icon2 = self.icon_asset_path+'grey_bus.png'
            
            
            offset = self.vertical_line.y()+35

            if previous_bus != None:
                offset = previous_bus.y()+previous_bus.height()+10
            
            b, w = self.create_sub_arrivals(self.wid,'bus_'+i, bus_icon1, bus_icon2, offset, i)
            self.bus_widget[i] = w
            previous_bus = b


        self.t_api.get_bus_arrival(self.bus_stop_code, self.busses)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.grab_data)
        self.timer.start(60000)

    def grab_data(self):
        self.t_api.get_bus_arrival(self.bus_stop_code, self.busses)

    def createImageLogo(self, master, objName, image_path, offset_x, offset_y, image_size, opacity):
        temp_icon_label = QtWidgets.QLabel(master, objectName = objName)
        temp_icon_label.setGeometry(offset_x, offset_y, image_size, image_size) 
        temp_icon_label.setStyleSheet("QLabel#"+temp_icon_label.objectName()+""
                                "{"
                                "background-color: rgba(255, 255, 255,"+str(opacity)+");"
                                "}")
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(temp_icon_label.width(), temp_icon_label.height(), QtCore.Qt.KeepAspectRatio)
        temp_icon_label.setPixmap(pixmap)
        return temp_icon_label
    
    def create_sub_arrivals(self, master, objName, image_path1, image_path2 , y, bus_service_no):
        

        wid_ = QtWidgets.QWidget(master, objectName = objName)
        wid_.setGeometry(10,y,self.widget_width-20, 40)
        wid_.setStyleSheet("QWidget#"+wid_.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(135,206,250, 0);"
                                #"border : 2px solid white;"
                                #"border-radius: 12px;"
                                "}")
        
        
        bus_service_no_label = QtWidgets.QLabel(wid_, objectName='bus_service_no', text=(bus_service_no)) 
        bus_service_no_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        bus_service_no_label.setGeometry(25, 0, 50, 40) 
        bus_service_no_label.setFont(QtGui.QFont('Roboto Black', 16)) 
        bus_service_no_label.setStyleSheet("QLabel#"+bus_service_no_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        
      
        next_bus = self.createImageLogo(wid_, objName+'_logo1', image_path1, bus_service_no_label.x()+bus_service_no_label.width()+5, 8, 24,0)
        next_bus2 = self.createImageLogo(wid_, objName+'_logo2', image_path2, bus_service_no_label.x()+bus_service_no_label.width()+120, 8, 24,0)

        arrival_1_label = QtWidgets.QLabel(wid_, objectName='nextBus_label', text='NIL') 
        arrival_1_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        arrival_1_label.setGeometry(next_bus.x()+next_bus.width()+10, 0, 50, 40) 
        arrival_1_label.setFont(QtGui.QFont('Roboto', 14)) 
        arrival_1_label.setStyleSheet("QLabel#"+arrival_1_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        
        arrival_2_label = QtWidgets.QLabel(wid_, objectName='nextBus2_label', text='NIL') 
        arrival_2_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        arrival_2_label.setGeometry(next_bus2.x()+next_bus2.width()+10, 0, 50, 40) 
        arrival_2_label.setFont(QtGui.QFont('Roboto', 14)) 
        arrival_2_label.setStyleSheet("QLabel#"+arrival_2_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        
        
        wid_.show()
        return wid_, {'NextBus':[next_bus,arrival_1_label], 'NextBus2':[next_bus2,arrival_2_label]}

    def setLabelImage(self, image_path, label):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(label.width(), label.height(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap (pixmap)
        return label

    def get_bus_load(self,data):
        bus_icon = "grey_bus"
        if data['Load'] == 'SEA':
            bus_icon = 'green_bus'
        elif data['Load'] == 'SDA':
            bus_icon = 'orange_bus'
        elif data['Load'] == 'LSD':
            bus_icon = 'red_bus'
        return bus_icon
        
    def updateLabels(self, data):
        if 'bus_arrival' in data:
            self.location_label.setText(data['bus_arrival']['bus_stop_name'])

            # previous_bus = None
            for i in data['bus_arrival']['results']:
                bus_icon1 = self.icon_asset_path+self.get_bus_load(i['NextBus'])+'.png'
                bus_icon2 = self.icon_asset_path+self.get_bus_load(i['NextBus2'])+'.png'
                tmp_bus_wid1 = self.bus_widget[i['ServiceNo']]['NextBus']
                tmp_bus_wid2 = self.bus_widget[i['ServiceNo']]['NextBus2']
                self.setLabelImage(bus_icon1, tmp_bus_wid1[0])
                self.setLabelImage(bus_icon2, tmp_bus_wid2[0])
                t1 = str(i['NextBus']['Time'])
                if len(t1) == 0:
                    tmp_bus_wid1[1].setText('NIL')
                else:
                    tmp_bus_wid1[1].setText(t1)
                    
                t2 = str(i['NextBus2']['Time'])
                if len(t2) == 0:
                    tmp_bus_wid2[1].setText('NIL')
                else:
                    tmp_bus_wid2[1].setText(t2)
                    

                
               
               
                




