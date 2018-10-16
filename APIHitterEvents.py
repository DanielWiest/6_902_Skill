import requests
import json

def fetchUpcomingMITEvents(numberOfEvents):
    
    
    badCharacters = {'@':' at ','&':' and ','%':' percent ','#':' number ','*':' ','(':' ',')':' ','/':' '}

    url = "http://m.mit.edu/apis/calendars/events_calendar/events"

    r = requests.get(url)

    data = json.loads(r.text)
    #print(data)

    outputText = "The next "+str(numberOfEvents)+" upcoming MIT events are "
    #print("The next",numberOfEvents, "upcoming MIT events are:\n")
    for event in data[:numberOfEvents]:
        #print(event['title'],'\n')
        outputText += event['title']+", "
        #print(event['title'],"at",event['start_at'],'\n')
    updatedString = list(outputText[:-2]+".")
    for index,char in enumerate(updatedString):
        if char in badCharacters:
            updatedString[index] = badCharacters[char]
    return "".join(updatedString)

#print(fetchUpcomingMITEvents(5))
