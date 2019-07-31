import os
import json

import GetNes
import GetOccupation


"""
Write a day's data to JSON
"""

def writeToJson(year, month, day):
    # year = sys.argv[1]
    month = month.zfill(2)
    day = day.zfill(2)

    # Create the day object
    dailyData = {}

    # From GetNes
    # !!!!!! Not Complete yet! Only store persons and sentiment value at present !!!!!!!!!!

    persons = GetNes.extractDailyInfo(year, month, day)[0]
    pairs = GetNes.extractDailyInfo(year, month, day)[4]
    axis = GetNes.extractDailyInfo(year, month, day)[3] # axis of heatmap
    links = GetNes.extractDailyInfo(year, month, day)[2]
    sentiment = GetNes.extractDailyInfo(year, month, day)[6]

    ## person counts

    personsArray = [] 

    for person in persons:
        pair = {"key": person[0], "count": person[1]}
        personsArray.append(pair)

    dailyData['persons'] = personsArray
    dailyData['sentiment'] = sentiment

    ## link counts

    linkArray = []
    nodeArray = [] # list of node items
    nodeList = [] # list of persons

    for pair in links.items():
        if pair[0][0] not in nodeList:
            nodeList.append(pair[0][0])
        if pair[0][1] not in nodeList:
            nodeList.append(pair[0][1])

        linkArray.append({"source": pair[0][0], "target": pair[0][1], "value": pair[1]})

    dailyData['links'] = linkArray

    for node in nodeList:
        nodeArray.append({"id": node})
    dailyData['nodes'] = nodeArray


    ## pair counts
    dailyData["axis"] = axis
    pairArray = []
    
    for pair in pairs.items():
        pairArray.append({"source": pair[0][0], "target": pair[0][1], "value": pair[1]})

    dailyData['pairs'] = pairArray


    # From GetOccupation

    occupationsArray= []

    for occ in GetOccupation.getDailyOccupations(list(dict(persons).keys()), year, month, day):
        pair = {"key": occ[0], "count": occ[1]}
        occupationsArray.append(pair)

    dailyData['occupations'] = occupationsArray


    # Export to JSON file
    directory = "json" # TO-BE-changed

    if not os.path.exists(directory):
        os.makedirs(directory)

    jsonName = '{}/{}-{}-{}.json'.format(directory, year, month, day)

    with open(jsonName, 'w') as f: # write mode will overwrite the original content
        json.dump(dailyData, f)


# MAIN

year = "2019"
month = "06"
# day = ["{}".format(i) for i in range(1,11)]

# for d in day:
#     writeToJson(year, month, d)

writeToJson("2019","6","1")