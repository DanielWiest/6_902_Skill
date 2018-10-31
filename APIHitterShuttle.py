import requests
import pprint
import time
import math
import json


def nextArrivalTimeAt(stringLocation):
    
    requestTime = time.time()
    
    stops = {'Kendall_Square_T':'01','77_Mass_Ave':'02','84_Mass_Ave':'03','vassar_street_mass_ave':'52','simmons':'47','W98_at_Vassar_St':'67'}

    baseURL = "http://m.mit.edu/apis/shuttles/predictions/?agency=mit&stop_number="
    urlAppended = baseURL+stops[stringLocation]
    
    r = requests.get(urlAppended)
    
    data = json.loads(r.text)
    
    #pprint.pprint(data)
    
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
            print("The",theRoute,"arrives at",hrTime,"at",route['stop_title'])
            print("This is in "+str(math.floor((timestamp-requestTime)/60))+" minutes.")
            outputText += "the "+theRoute+" arrives at "+route['stop_title']+" in "+str(math.floor((timestamp-requestTime)/60))+" minutes. Also, "
    
    if not atLeastOneRouteTo:
        print("No routes serving "+stringLocation+" at this time.")
        return "There are no routes serving "+stringLocation+" at this time."
    else:
        return outputText[:-7]

#nextArrivalTimeAt('Kendall Square T')
#nextArrivalTimeAt('77 Mass Ave')
#nextArrivalTimeAt('84 Mass Ave')