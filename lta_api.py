from geopy.geocoders import Nominatim
import json
import sys
from math import cos, asin, sqrt
from requester import RequestHandler
from PyQt5 import QtCore, QtGui, QtNetwork
from math import sqrt
from datetime import datetime
import calendar 
import os.path

# this class mainly handles and format the replies from requests
# if there is a change in API response structure, this needs to be re-coded


# TODO: Calculate arrival time...Need to handle when no estimation or unavailable... just show NIL

class TransportAPI(object):
  

    # URLs
    bus_arrival_url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
    API_key = 'YOUR_API_KEY_HERE'
   

    # files
    bus_stops_file = 'bus_stops.json'

    # data
    bus_stops_data = None
    
    def __init__(self, master, callback_):
        self.master = master
        self.callback_ = callback_
        self.r = RequestHandler(self.master)
        self.init_bus_stop_name()
      
        
    
    def init_bus_stop_name(self):
        # check if bus stop file is there
        if os.path.isfile(self.bus_stops_file):
            with open(self.bus_stops_file) as json_file:
                self.bus_stops_data = json.load(json_file)

    

    def get_bus_arrival(self, bus_stop_code, busses):
        def callback_j(reply):
            er = reply.error()
            
            if er == QtNetwork.QNetworkReply.NoError:
                bytes_string = reply.readAll()
                data = json.loads(str(bytes_string, 'utf-8'))
                #print(data)
                bus_stop_name = "Error"
                if self.bus_stops_data != None:
                    if bus_stop_code in self.bus_stops_data:
                        bus_stop_name = self.bus_stops_data[bus_stop_code]


                results = self.process_bus_arrival(data, busses)
                #print(results)
                #print(data)
                self.callback_({'bus_arrival':{'bus_stop_name':bus_stop_name,'results':results}})
               
            else:
                print("Error occured: ", er)
                print(reply.errorString())
    
        headers_ = {'AccountKey':self.API_key}
        self.r.doRequest(callback_j,self.bus_arrival_url+'?BusStopCode='+bus_stop_code,headers_)

    def process_bus_arrival(self, data, busses):
        results = []
        _busses = busses.copy() # to hold busses that failed to query
        # Get current time here, then find difference between EstimatedArrival
        d,t = self.current_datetime()
        for i in data['Services']:
            if i['ServiceNo'] in busses:
                if i['NextBus']['EstimatedArrival'] == '':
                    time_diff1 = 'NIL'
                else:    
                    time_diff1 = (self.find_datetime_diff(i['NextBus']['EstimatedArrival'][:-9].replace('T',' '),d+" "+t[:-3]))
                    if time_diff1 <= 0:
                        time_diff1 = 'Arr'
                if i['NextBus2']['EstimatedArrival'] == '':
                    time_diff2 = 'NIL'
                else:
                    time_diff2 = (self.find_datetime_diff(i['NextBus2']['EstimatedArrival'][:-9].replace('T',' '),d+" "+t[:-3]))
                    if time_diff2 <= 0:
                        time_diff2 = 'Arr'
                

                tmp = {'ServiceNo':i['ServiceNo'],
                        'NextBus':{'Time':time_diff1,'Load':i['NextBus']['Load'],'Type':i['NextBus']['Type']},
                        'NextBus2':{'Time':time_diff2,'Load':i['NextBus2']['Load'],'Type':i['NextBus2']['Type']}
                        }
                _busses.remove(i['ServiceNo'])
                results.append(tmp)

        # Busses that are not found in the response
        for f in _busses:
            tmp = {'ServiceNo':f,
                    'NextBus':{'Time':'', 'Load':'', 'Type':''},
                    'NextBus2':{'Time':'', 'Load':'', 'Type':''}
                    }
            results.append(tmp)
        
        return results

    def current_datetime(self):
        now = datetime.now()
        d = str(now.strftime("%Y-%m-%d"))
        t = str(now.strftime("%H:%M:%S"))
        return d,t
    
    def find_datetime_diff(self, dt2, dt1):
       
        FMT = '%Y-%m-%d %H:%M'
        tdelta = datetime.strptime(dt2, FMT) - datetime.strptime(dt1, FMT)
        
        return int(tdelta.total_seconds()/60)