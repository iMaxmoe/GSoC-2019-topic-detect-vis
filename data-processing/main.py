import os, json, sys, datetime

from datetime import datetime, timedelta

import GetNes, GetOccupation
from pymongo import MongoClient


def writeToDb(path, year, month, day, db):
    month = str(month).zfill(2)
    day = str(day).zfill(2)

    # Create the day object
    dailyData = {}
    dailyData['date'] = datetime.strptime('{}-{}-{}'.format(year, month, day), "%Y-%m-%d")

    persons, organizations, links, axis, pairs, locations, sentiment = GetNes.extractDailyInfo(path, year, month, day, db)

    # person counts
    personsArray = [] 

    for person in persons:
        pair = {"key": person[0], "count": person[1]}
        personsArray.append(pair)

    dailyData['persons'] = personsArray
    dailyData['sentiment'] = sentiment

    # link counts

    linkArray = []
    nodeArray = [] # list of node items
    nodeList = [] # list of persons

    for pair in links.items():
        if pair[0][0] not in nodeList:
            nodeList.append(pair[0][0])
        if pair[0][1] not in nodeList:
            nodeList.append(pair[0][1])

        linkArray.append({ "source": pair[0][0], "target": pair[0][1], "value": pair[1] })

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


    # Export to db
    byDate = db.byDate
    byDate.insert_one(dailyData)
    dateList = db.dateList
    dateList.insert_one({ "date": dailyData['date'] })

# MAIN

year, month, day = sys.argv[1:4]
month, day = month.zfill(2), day.zfill(2)

path = sys.argv[4] # absolute path prefix

start_date = datetime.strptime("2019-08-01", '%Y-%m-%d')
end_date = "{}-{}-{}".format(year, month, day)
end_date = datetime.strptime(end_date, '%Y-%m-%d')

step = timedelta(days=1)
date_list = []

while start_date <= end_date:
    date_list.append(start_date.date())
    start_date += step
    
client = MongoClient('localhost', 27017)
db = client["news"]

for d in date_list:
    dateList = db.dateList # a collection of dates
    d_datetime = datetime.strptime(d.strftime("%Y-%m-%d"), '%Y-%m-%d')
    if dateList.count({ "date": d_datetime }) != 0:
        print("{} is already in database, go to next one".format(d.strftime("%Y-%m-%d")))
    else:   
        writeToDb(path, d.year, d.month, d.day, db)
