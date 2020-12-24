from geopy.geocoders import Nominatim
import json
import sys
from math import cos, asin, sqrt
from requester import RequestHandler
from PyQt5 import QtCore, QtGui, QtNetwork
from math import sqrt
import datetime
import calendar 
import os.path

# this class mainly handles and format the replies from requests
# if there is a change in API response structure, this needs to be re-coded

class WeatherAPI(object):
   
    # Example of my_locations dictionary:

    # my_locations = {'Marine Parade':None,
    #                 'NUS': {'location':{'latitude':1.2962018, 'longitude': 103.77689943784759},
    #                         'correspond_station':{'id': 'S116', 'device_id': 'S116', 'name': 'West Coast Highway', 'location': {'latitude': 1.281, 'longitude': 103.754}}},
    #                 'Sengkang':None}
    
    my_locations = {}
    
    weather_stations = []
    country = 'Singapore'
    num_of_loc = 0
    weather_json_file = 'weather_data.json'

    # URLs
    NEA_base_url = 'https://api.data.gov.sg/v1/environment/'
    four_days_forecast = '4-day-weather-forecast'
    general_forecast = '24-hour-weather-forecast'
    air_temp = 'air-temperature'
    weather_icon_url = 'http://www.weather.gov.sg/weather-forecast-4dayoutlook/'
    
    def __init__(self, master, callback_):
        #self.API_key = API_key
        self.master = master
        self.callback_ = callback_
        self.r = RequestHandler(self.master)
        self.check_config_file()
       
    
    def check_config_file(self):

        if os.path.isfile(self.weather_json_file) == False:
            f= open(self.weather_json_file,"w+")
            f.write("{}")
            f.close()
        
        with open(self.weather_json_file) as json_file:
            self.my_locations = json.load(json_file)
            
        
        self.num_of_loc = 0
        f = open("weather_locations.txt", "r")
        correct = True
        for x in f:
            x = x.rstrip()
            self.num_of_loc = self.num_of_loc + 1
            if x not in self.my_locations:
                correct= False
                self.my_locations[x] = None
                #print(x,'not in my_locations')
                
        if correct == False:
            self.populate_my_locations()
            self.get_weather_station()
        f.close()
        return correct
        
    def get_forecast_weather_icons(self):
        def callback_j(reply):
            er = reply.error()
            
            if er == QtNetwork.QNetworkReply.NoError:
                bytes_string = reply.readAll()
                data = (str(bytes_string, 'utf-8'))
                results = self.process_weather_icons(data.splitlines())
               
                self.callback_({'forecast_icons':results})
            else:
                print("Error occured: ", er)
                print(reply.errorString())
    
        self.r.doRequest(callback_j,self.weather_icon_url)


    def process_weather_icons(self, data):
        left = 'http://www.weather.gov.sg/wp-content/themes/wiptheme/assets/img/'
        right = '.png'
        results = []
        for i in data:
            if 'wicon wicon-weather' in i:
                s = i.split("wicon wicon-weather")
                if len(s) > 1:
                    results.append(s[1][s[1].index(left)+len(left):s[1].index(right)].replace("-small","").replace("icon-",""))
        return results

    def get_weather_station(self, filtered=False):
        
        def callback_f(reply):
            er = reply.error()
            
            if er == QtNetwork.QNetworkReply.NoError:
                bytes_string = reply.readAll()
                json_data = json.loads(str(bytes_string, 'utf-8'))
                
                self.weather_stations = self.process_weather_stations(json_data)
                
                if filtered == True:
                    filtered_results = []
                    for k,v in self.my_locations.items():                       
                       for b in self.weather_stations:
                           if b['id'] == v['correspond_station']['id']:
                               res = {k:b['temperature']}
                               filtered_results.append(res)
                               break
                    if len(filtered_results) == self.num_of_loc:
                        self.callback_({'current_temperature':filtered_results})
                    else: 
                        print('Missing weather station, finding nearest one')
                        self.get_weather_station()
                       

                if filtered == False:
                    loc = [i['location'] for i in self.weather_stations]
                    
                    # find nearest corresponding weather station
                    for k,v in self.my_locations.items():
                        #if self.my_locations[k]['correspond_station'] == None:
                        a = v['location']
                        closest_ = self.closest(loc,a)
                        corresponding_ = [i for i in self.weather_stations if i['location'] == closest_]
                        self.my_locations[k]['correspond_station'] = corresponding_[0]
                        
                    # Write json to file..
                    with open('weather_data.json', 'w') as outfile:
                        json.dump(self.my_locations, outfile, indent=4)
                    
                
            else:
                print("Error occured: ", er)
                print(reply.errorString())

        d,t = self.current_datetime()
        param_ = "?date_time="+str(d)+"T"+str(t)[:-2].replace(":","%3A")+"00"
        self.r.doRequest(callback_f,self.NEA_base_url+self.air_temp+param_)

    def process_weather_stations(self,data):
        results = []
        for i in data['metadata']['stations']:
            for b in data['items'][0]['readings']:
                if b['station_id'] == i['id']:
                    i['temperature']=b['value']
                    break
         
            results.append(i)  
        return results

    def get_general_forecast(self):
        def callback_j(reply):
            er = reply.error()
            
            if er == QtNetwork.QNetworkReply.NoError:
                bytes_string = reply.readAll()
                data = json.loads(str(bytes_string, 'utf-8'))
               
                self.callback_({'general_forecast':data['items'][0]['general']})
            else:
                print("Error occured: ", er)
                print(reply.errorString())
    
        d,t = self.current_datetime()
        param_ = "?date_time="+str(d)+"T"+str(t)[:-2].replace(":","%3A")+"00"
        self.r.doRequest(callback_j,self.NEA_base_url+self.general_forecast+param_)

    def get_forecast(self):
        def callback_j(reply):
            er = reply.error()
            
            if er == QtNetwork.QNetworkReply.NoError:
                bytes_string = reply.readAll()
                data = (str(bytes_string, 'utf-8'))
                results = self.process_forecast(json.loads(data))
              
                #print(results)
                self.callback_({'four_days_forecast':results['forecasts']})
            else:
                print("Error occured: ", er)
                print(reply.errorString())
    
        d,t = self.current_datetime()
        param_ = "?date_time="+str(d)+"T"+str(t)[:-2].replace(":","%3A")+"00"
        self.r.doRequest(callback_j,self.NEA_base_url+self.four_days_forecast+param_)
        
    def process_forecast(self, data):
        results = []
        for i in data['items'][0]['forecasts']:
            result= {'temperature':'\t'+str(i['temperature']['low'])+" °C\n\t"+str(i['temperature']['high'])+" °C",
                        'date':self.findDay(str(i['date']))[0:3].upper(),
                        'forecast':i['forecast']}
            results.append(result)
        return {'forecasts':results}
   
    
    def populate_my_locations(self):
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        for k,v in self.my_locations.items():
            if v == None:
                location = geolocator.geocode(str(k)+","+self.country)
                self.my_locations[k] = {'location':{'latitude':location.latitude, 'longitude':location.longitude},
                                        'correspond_station':None}
                print(location.address)
                print((location.latitude, location.longitude))




    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))

    def closest(self, data, v):
        return min(data, key=lambda p: self.distance(v['latitude'],v['longitude'],p['latitude'],p['longitude']))

    def current_datetime(self):
        now = datetime.datetime.now()
        d = str(now.strftime("%Y-%m-%d"))
        t = str(now.strftime("%H:%M:%S"))
        return d,t

    def findDay(self, date): 
        born = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
        return (calendar.day_name[born]) 

    def get_am_pm(self):
        return str(datetime.datetime.now().strftime("%p"))
    
