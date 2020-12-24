
import functools

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtNetwork
from weather_api import WeatherAPI
import os.path


class Weather_Widget:
    
    # User settings
    icon_asset_path = './assets/nea_icons/'
    no_of_days_to_forecast = 3
    animation_delay = 5500
    grab_data_delay = 360000 # 30minutes
    show_last_updated = True
    # end of settings
    
    nocturnal_icons = ['fair','partly-cloudy']
    
    current_temperature = []
    location_index = 0

    
    received_data = {'general_forecast':False,
                     'current_temperature':False,
                     'four_days_forecast':False,
                     'forecast_icons':False}
    

    def __init__(self, master): 
        widget_width = 450
        
        self.master = master
        self.w_api = WeatherAPI(master, self.updateLabels)
        
        self.timer = QtCore.QTimer(master)
        self.timer.timeout.connect(self.animate_)
        self.timer.start(self.animation_delay)

        self.timer_grab_data = QtCore.QTimer(master)
        self.timer_grab_data.timeout.connect(self.grab_data)
        self.timer_grab_data.start(self.grab_data_delay)

        

        wid_frame = QtWidgets.QWidget(master, objectName = "weather_widget_frame")
        wid_frame.setGeometry(10,10,500,650)
        wid_frame.setStyleSheet("QWidget#"+wid_frame.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(0,0,0,0);"
                                "border-radius: 12px;"
                                "}")
        wid_frame.mouseMoveEvent = functools.partial(master.movementHandler, source_object=wid_frame)


        
        

        wid = QtWidgets.QWidget(wid_frame, objectName = "weather_widget")
        wid.setGeometry(10,0,widget_width,175)
        wid.setStyleSheet("QWidget#"+wid.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                #"background-color: rgba(135,206,250, 180);"
                                "background-color: rgba(135,108,108, 255);"
                                "border : 2px solid white;"
                                "border-radius: 12px;"
                                "}")
        
       

     
        # Left panel
        self.weather_logo = self.createImageLogo(wid, 'current_weather_logo', './assets/nea_icons/unknown.png', 70, 40, 75,0)
        self.weather_label = QtWidgets.QLabel(wid, objectName='weather_label', text='Thunderstorm') 
        self.weather_label.setAlignment(QtCore.Qt.AlignCenter)
        self.weather_label.setGeometry(self.weather_logo.x()-50, self.weather_logo.y()+55, 180, 90) 
        self.weather_label.setFont(QtGui.QFont('Roboto Medium', 14)) 
        self.weather_label.setStyleSheet("QLabel#"+self.weather_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")

        # Right panel
        self.wid_r_panel = QtWidgets.QWidget(wid_frame, objectName = "weather_right_panel")
        self.wid_r_panel.setGeometry(10,10,500,400)
        self.wid_r_panel.setStyleSheet("QWidget#"+self.wid_r_panel.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(0,0,0,0);"
                                "}")

        self.location_label = QtWidgets.QLabel(self.wid_r_panel, objectName='location_label', text='...') 
        self.location_label.setAlignment(QtCore.Qt.AlignCenter)
        self.location_label.setGeometry(wid.x()+180, wid.y()+15, 250, 40) 
        self.location_label.setFont(QtGui.QFont('Roboto', 16)) 
        self.location_label.setStyleSheet("QLabel#"+self.location_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")

        self.temperature_label = QtWidgets.QLabel(self.wid_r_panel, objectName='temperature_label', text='...') 
        self.temperature_label.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_label.setGeometry(wid.x()+180, self.location_label.y()+40, 250, 60) 
        self.temperature_label.setFont(QtGui.QFont('Roboto Medium', 42)) 
        self.temperature_label.setStyleSheet("QLabel#"+self.temperature_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        self.hl_temperature_label = QtWidgets.QLabel(wid, objectName='hl_temperature_label', text='...') 
        self.hl_temperature_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hl_temperature_label.setGeometry(self.temperature_label.x(), self.temperature_label.y()+70, 250, 30) 
        self.hl_temperature_label.setFont(QtGui.QFont('Roboto', 12)) 
        self.hl_temperature_label.setStyleSheet("QLabel#"+self.hl_temperature_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")

        # Generate x days forecasts
        self.forecast_labels = []
        self.forecast_logos = []
        previous_wid = wid
        for i in range(0,self.no_of_days_to_forecast):
            wid_day, forecast_day_logo, labels_ = self.create_mini_widget(wid_frame, 'weather_forecast_day'+str(i), "./assets/nea_icons/unknown.png", (previous_wid.y()+previous_wid.height()+10),widget_width, '...','...','...')
            self.forecast_labels.append(labels_)
            self.forecast_logos.append(forecast_day_logo)
            previous_wid = wid_day
        
        if self.show_last_updated:
            self.last_updated_label = QtWidgets.QLabel(wid_frame, objectName='last_updated_label', text='last updated: ') 
            self.last_updated_label.setAlignment(QtCore.Qt.AlignLeft)
            self.last_updated_label.setGeometry(20, previous_wid.y()+previous_wid.height()+10, 250, 30) 
            self.last_updated_label.setFont(QtGui.QFont('Roboto', 10)) 
            self.last_updated_label.setStyleSheet("QLabel#"+self.last_updated_label.objectName()+""
                                    "{"
                                    "color: lime;"
                                    "background-color: rgba(255, 255, 255,0);"
                                    "}")

        
        self.w_api.get_weather_station(True)
        self.w_api.get_general_forecast()
        self.w_api.get_forecast_weather_icons()
        self.w_api.get_forecast()
        if self.show_last_updated:
            _,t = self.w_api.current_datetime()
            self.last_updated_label.setText('last updated: '+str(t))

        



        
        # b4 = QtWidgets.QPushButton(wid_frame, text="&Default", objectName = 'aa')
        # b4.setGeometry(0,0,300,300)
        # #b4.setDefault(True)
        # b4.setStyleSheet("QPushButton#"+b4.objectName()+""
        #                         "{"
        #                         "color: white;"
        #                         "background-color: rgba(255, 255, 255,255);"
        #                         "}")
        # b4.clicked.connect(lambda:self.updateData(master))


    
   
    

    def setLabelImage(self, image_path, label):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(label.width(), label.height(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap (pixmap)
        return label

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

    def create_mini_widget(self, master, objName, image_path, y, widget_width, day_string, temperature_string, forecast_string):
        wid_day1 = QtWidgets.QWidget(master, objectName = objName)
        wid_day1.setGeometry(10,y,widget_width, 90)
        wid_day1.setStyleSheet("QWidget#"+wid_day1.objectName()+""       # To ensure stylesheet only applies to parent
                                "{"
                                "background-color: rgba(135,206,250, 180);"
                                "border : 2px solid white;"
                                "border-radius: 12px;"
                                "}")
        # (wid_day1.y()*-1)+7
        forecast_day1_logo = self.createImageLogo(wid_day1, objName+'_logo', image_path, 10, 7, 75,0)

        day_label = QtWidgets.QLabel(master, objectName='day_label', text=day_string) 
        day_label.setAlignment(QtCore.Qt.AlignLeft)
        day_label.setGeometry(forecast_day1_logo.x()+110, wid_day1.y()+10, 250, 40) 
        day_label.setFont(QtGui.QFont('Roboto Medium', 18)) 
        day_label.setStyleSheet("QLabel#"+day_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
        
        temperature_label = QtWidgets.QLabel(master, objectName='temperature_label', text=temperature_string) 
        temperature_label.setAlignment(QtCore.Qt.AlignLeft)
        temperature_label.setGeometry(day_label.x()-55, day_label.y()+day_label.height()-10, 120, 40) 
        temperature_label.setFont(QtGui.QFont('Roboto', 11)) 
        temperature_label.setStyleSheet("QLabel#"+temperature_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")

        forecast_label = QtWidgets.QLabel(master, objectName='forecast_label', text=forecast_string) 
        forecast_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        forecast_label.setWordWrap(True)
        forecast_label.setGeometry(day_label.x()+85, day_label.y(), 220, 70) 
        forecast_label.setFont(QtGui.QFont('Roboto Light', 13)) 
        forecast_label.setStyleSheet("QLabel#"+forecast_label.objectName()+""
                                "{"
                                "color: white;"
                                "background-color: rgba(255, 255, 255,0);"
                                "}")
    


        return wid_day1, forecast_day1_logo, [temperature_label ,day_label, forecast_label]


    def grab_data(self):
        self.w_api.get_weather_station(True)
        self.w_api.get_general_forecast()
        self.w_api.get_forecast_weather_icons()
        self.w_api.get_forecast()

        if self.show_last_updated:
            _,t = self.w_api.current_datetime()
            self.last_updated_label.setText('last updated: '+str(t))


    def animate_(self): 
        all_received = True
        for k,v in self.received_data.items():
            if v == False:
                all_received=v
        
        if all_received == True:
            self.location_index = self.location_index + 1
            if self.location_index >= len(self.current_temperature):
                self.location_index = 0
            wid_list = [self.temperature_label, self.location_label]
            text_list = [str(list(self.current_temperature[self.location_index].values())[0])+" °C",
                        str(list(self.current_temperature[self.location_index].keys())[0])]
            self.fade(self.wid_r_panel, wid_list, text_list)
            # if self.show_last_updated:
            #     _,t = self.w_api.current_datetime()
            #     self.last_updated_label.setText('last updated: '+str(t))


    # def updateData(self,master):
    #     print('in updateData')
     

    def updateLabels(self, data):
        if 'general_forecast' in data:
            hl = data['general_forecast']['temperature'] # getting daily temperature's high-low
            forecast_text = data['general_forecast']['forecast'].lower().replace(" ","-")
            
            # check if the forecast is have nocturnal icons 
            # e.g partly-cloudly-day or partly-cloudly-night

            if forecast_text in self.nocturnal_icons:
                am_pm = self.w_api.get_am_pm()
                if am_pm == 'PM':
                    forecast_text = forecast_text + '-night'
                elif am_pm == 'AM':
                    forecast_text = forecast_text + '-day'

            # check if the icon asset exists (precautionary)
            if os.path.isfile(self.icon_asset_path+forecast_text+'.png'):
                self.setLabelImage(self.icon_asset_path+forecast_text+'.png',self.weather_logo)
            else:
                self.setLabelImage(self.icon_asset_path+'unknown.png',self.weather_logo)

            self.hl_temperature_label.setText("L: "+str(hl['low'])+" °C  |  H: "+str(hl['high'])+" °C")
            self.weather_label.setText(str(data['general_forecast']['forecast']))
            self.received_data['general_forecast'] = True
        
        if 'four_days_forecast' in data:
            forecasts = data['four_days_forecast']

            for i in range(0, len(self.forecast_labels)):
                self.forecast_labels[i][0].setText(forecasts[i]['temperature'])
                self.forecast_labels[i][1].setText(forecasts[i]['date'])
                self.forecast_labels[i][2].setText(forecasts[i]['forecast'])

            self.received_data['four_days_forecast'] = True

        if 'forecast_icons' in data:
            for i in range(0,len(self.forecast_logos)):
                file_path = self.icon_asset_path + data['forecast_icons'][i] + '.png'
                # check if the icon asset exists (precautionary)
                if os.path.isfile(file_path):
                    self.setLabelImage(file_path,self.forecast_logos[i])
                else:
                    self.setLabelImage(self.icon_asset_path+'unknown.png',self.forecast_logos[i])
            self.received_data['forecast_icons'] = True

        if 'current_temperature' in data:
            self.current_temperature = data['current_temperature']
            self.received_data['current_temperature'] = True
            
    def fade(self, frame, widget, next_text):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        
        frame.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(600)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self.animation.finished.connect(lambda: self.update_and_unfade(frame, widget, next_text))

    def unfade(self, frame, widget):
        self.effect =  QtWidgets.QGraphicsOpacityEffect()
        
        frame.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(600)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.animation.finished.connect(lambda: self.updateFrame(frame))
       
    def updateFrame(self,widget):
        # to prevent the current location + temperature label to move out of frame after animation (bug?)
        widget.hide()
        widget.show()

    def update_and_unfade(self, frame, widget, next_text):
        for i in range(0, len(widget)):
            widget[i].setText(next_text[i])
        self.unfade(frame, widget)

   
    
   