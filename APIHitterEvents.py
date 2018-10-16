import requests
import json

def fetchUpcomingMITEvents(numberOfEvents):

    url = "http://m.mit.edu/apis/calendars/events_calendar/events"

    r = requests.get(url)

    data = json.loads(r.text)
    print(data)

    outputText = "The next "+str(numberOfEvents)+" upcoming MIT events are "
    print("The next",numberOfEvents, "upcoming MIT events are:\n")
    for event in data[:numberOfEvents]:
        print(event['title'],'\n')
        outputText += event['title']+", "
        #print(event['title'],"at",event['start_at'],'\n')
    return outputText[:-2]+"."

print(fetchUpcomingMITEvents(5))
