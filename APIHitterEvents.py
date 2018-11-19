import requests
import json
from dateutil import parser
import datetime

def fetchUpcomingMITEvents(numberOfEvents):
    
    
    badCharacters = {'@':' at ','&':' and ','%':' percent ','#':' number ','*':' ','(':' ',')':' ','/':' '}

    url = "http://m.mit.edu/apis/calendars/events_calendar/events"

    r = requests.get(url)
    numLoops = 0
    eventsAdded = 0 

    data = json.loads(r.text)
    #print(data)
    timeNow = datetime.datetime.now().timestamp()

    outputText = "The next "+str(numberOfEvents)+" upcoming MIT events are "
    #print("The next",numberOfEvents, "upcoming MIT events are:\n")
    options = list(data)
    while eventsAdded < numberOfEvents and numLoops < min(100,len(options)):
        
        event = options[numLoops]
        eventTime = event['start_at']
        formattedTime = parser.parse(eventTime)
        ts = formattedTime.timestamp()
        
        secondsTill = ts - timeNow
        minTill = secondsTill/60
        
        if minTill > 0:
            if minTill > 45:
                outputText += event['title']+", which starts in "+str(round(minTill/60,1))+" hours, "
            else:
                outputText += event['title']+", which starts in "+str(round(minTill,1))+" minutes, "
            eventsAdded += 1
            
        numLoops += 1
    updatedString = list(outputText[:-2]+".")
    for index,char in enumerate(updatedString):
        if char in badCharacters:
            updatedString[index] = badCharacters[char]
    return "".join(updatedString)

#print(fetchUpcomingMITEvents(5))
