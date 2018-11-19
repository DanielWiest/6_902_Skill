import requests
import time

import math
import json


def nextArrivalTimeAt(stringLocation):
    
    requestTime = time.time()
    currentHour = int(time.strftime('%H'))
    
    if currentHour >= 23 or currentHour <= 3:
        return "Fixed route shuttles are not running at this time, however, you could try using the Trans Lock Rider mobile application in order to call the shuttle on demand."
    else:
        stops = {'Kendall_Square_T':'1','77_Mass_Ave':'2','84_Mass_Ave':'3','media_lab':'7','beacon_street':'13','478__commonwealth_ave': '21', '487_commonwealth_ave': '22', 'Edgerton': '23', 'simmons':'47', '500_Main': '48', 'tang_westgate': '51','vassar_street_mass_ave':'52','pacific_st_albany_st': '54', 'W92_amesbury_st': '57', 'commonwealth_sherbron': '59', 'amherst_at_kresge': '61','W98_at_Vassar_St':'67'}
    
        baseURL = "http://m.mit.edu/apis/shuttles/predictions/?agency=mit&stop_number="
        urlAppended = baseURL+stops[stringLocation]
        
        r = requests.get(urlAppended)
        
        data = json.loads(r.text)
        
        outputText = ""
        
        atLeastOneRouteTo = False
        for route in data:
            if route['predictable']:
                atLeastOneRouteTo = True
                theRoute = route['route_title']
                currentShuttles = route['predictions']
                print(theRoute,"is running!") 
                nextShuttle = currentShuttles[0]
                timestamp = nextShuttle['timestamp']
                hrTime = time.strftime("%H:%M:%S", time.localtime(timestamp))
                outputText += "the "+theRoute+" arrives at "+route['stop_title']+" in "+str(math.floor((timestamp-requestTime)/60))+" minutes. Also, "
        
        if not atLeastOneRouteTo:
            return "There are no routes serving "+stringLocation+" at this time."
        else:
            return outputText[:-7]

#print(nextArrivalTimeAt('Kendall_Square_T'))
#print(nextArrivalTimeAt('77_Mass_Ave'))
#print(nextArrivalTimeAt('84_Mass_Ave'))