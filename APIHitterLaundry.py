import requests


def getLaundryStatus(dormString,washer,dryer):
    
    outputString = ""
    
    dorms = {"baker":136484,"maseeh":1364830,'mccormik':136487,"burton-connor":1364811,"macgregor":1364815,"next-house":1364812}
    
    baseURL = "http://classic.laundryview.com/appliance_status_ajax.php?lr="
    
    appendedURL = baseURL+str(dorms[dormString])
    
    r = requests.get(appendedURL)
    theText = r.text
    
    washersIndex = theText.find("WASHERS")
    dryersIndex = theText.find("DRYERS")
    
    washersString = []
    dryersString = []
    for char in theText[washersIndex+16:]:
        washersString.append(char)
        if char == 'e':
            break
    for char in theText[dryersIndex+15:]:
        dryersString.append(char)
        if char == 'e':
            break
    washersString = "".join(washersString)
    dryersString = "".join(dryersString)
    
    resultWasher = "there are currently "+washersString+" washing machines in "+dormString
    resultDryer = "there are currently "+dryersString+" dryers in "+dormString
    
    if washer and dryer :
        outputString += resultWasher+" and " + resultDryer
        print(resultWasher,resultDryer)
    else:
        if dryer:
            outputString +=resultDryer
            print(resultDryer)
        if washer:
            outputString +=resultWasher
            print(resultWasher)
    print()
    return outputString+"."

#print(getLaundryStatus("baker",True,True))
#getLaundryStatus("maseeh",True,True)
#getLaundryStatus("mccormik",True,True)