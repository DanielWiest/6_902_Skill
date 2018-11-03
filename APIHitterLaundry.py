import requests

def getLaundryStatus(dormString,washer,dryer):
    
    outputString = ""
    
    dorms = {"baker":136484,"maseeh":1364830,'mccormik':136487,"burton-connor":1364811,"macgregor":1364815,"next-house":1364812}
    
    baseURL = "https://www.laundryview.com/api/currentRoomData?school_desc_key=74&location="
    
    appendedURL = baseURL+str(dorms[dormString])
    
    r = requests.get(appendedURL)
    theJson = r.json()
    numWashers = 0
    numWashersAvail = 0
    numDryers = 0
    numDryersAvail = 0
    for machine in theJson["objects"]:
        if machine["type"] == "washFL":
            numWashers += 1
            if machine["status_toggle"] == 0:
                numWashersAvail += 1
        elif machine["type"] == "dblDry":
            numDryers += 2
            if machine["status_toggle"] == 0:
                numDryersAvail += 1
            if machine["status_toggle2"] == 0:
                numDryersAvail += 1
    if washer:
        return "There are currently "+str(numWashersAvail)+" out of "+str(numWashers)+" washing machines available in "+dormString+"."
    elif dryer:
        return "There are currently "+str(numDryersAvail)+" out of "+str(numDryers)+" dryers available in "+dormString+"."
    else:
        return "No status was queried."
    return outputString+"."
