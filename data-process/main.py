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
    personPairs = GetNes.extractDailyInfo(year, month, day)[2]
    sentiment = GetNes.extractDailyInfo(year, month, day)[4]

    ## person counts

    personsArray = [] 

    for person in persons:
        pair = {"key": person[0], "count": person[1]}
        personsArray.append(pair)

    dailyData['persons'] = personsArray
    dailyData['sentiment'] = sentiment

    ## person pair counts

    pairArray = []

    x_axis = []
    y_axis = []

    for pair in personPairs:

        if pair[0][0] not in x_axis:
            x_axis.append(pair[0][0])
        if pair[0][1] not in y_axis:
            y_axis.append(pair[0][1])

        tuple_ = {"A": pair[0][0], "B": pair[0][1], "count": pair[1]}
        pairArray.append(tuple_)

    dailyData['pairs'] = pairArray
    dailyData['pairX'] = x_axis
    dailyData['pairY'] = y_axis


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
day = ["{}".format(i) for i in range(1,11)]

for d in day:
    writeToJson(year, month, d)