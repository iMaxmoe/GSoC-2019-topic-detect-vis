#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Process daily SEG files to get NE counts
"""

import re
import sys
import glob

def extractInfo(segPath, persons, organizations, locations, personPairs):
    """
    Extract the required information from a given file specified by segPath
    """
    try:
        with open(segPath, 'r', encoding='UTF-8', errors='ignore') as f:
            
            allLines = f.readlines()
            sentiment = [0,0] #(sentiment value amount, sentiment word counts)
            
            personList = list() # Persons mentioned in one news; temp storage
                       
            for line in allLines:

                # Check whether the file is written in English, if not, skip it
                if line.startswith("LAN|") or line.startswith("CC1|"):
                    if line != "LAN|ENG\n" and line != "CC1|ENG\n":
                        return
                
                # The content starts
                if line[0].isdigit():
                    parts = line.split('|')

                    # Get persons mentioned in the same news
                    if parts[2]=='SEG_02' and parts[3]=='Type=Story':
                        
                        # Generate all pairs from person list
                        if personList != []:
                            for i in range(len(personList)-1):
                                for j in range(i+1, len(personList)):

                                    # Make sure there is no equivalent pair, since(a,b)<=>(b,a)
                                    if personList[i] < personList[j]: # Alphabetic order
                                        pair = (personList[i], personList[j])
                                    else:
                                        pair = (personList[j], personList[i])

                                    if pair in personPairs:
                                        personPairs[pair] += 1
                                    else:
                                        personPairs[pair] = 1
                                        
                            personList = [] # Start a new collection
                            
                    # Get NER (PERSON, ORGANIZATION, LOCATION)
                    if parts[2]=='NER_03':
                        for part in parts:
                            if part.startswith('ORGANIZATION='):
                                org = part.split('=')[1].strip('\n')
                                if org in organizations:
                                    organizations[org] += 1
                                else:
                                    organizations[org] = 1
                                continue
                                
                            if part.startswith('LOCATION='):
                                loc = part.split('=')[1].strip('\n')
                                if loc in locations:
                                    locations[loc] += 1
                                else:
                                    locations[loc] = 1
                                continue
                                
                            if part.startswith('PERSON='):
                                ppl = part.split('=')[1].strip('\n')
                                tempP = ""
                                for p in ppl.split():
                                    p = p.lower().capitalize()
                                    tempP += p
                                    tempP += ' '
                                ppl = tempP[:-1]
                                
                                # We only collect full names for the sake of accuracy
                                if len(ppl.split()) < 2:
                                    continue
                                    
                                # For the sake of person pairs
                                if ppl not in personList:
                                    personList.append(ppl)
                                
                                # For the sake of person counts
                                if ppl in persons:
                                    persons[ppl] += 1
                                else:
                                    persons[ppl] = 1
                                continue
                                
                    # Get sentiment
                    if parts[2]=='SMT_02':

                        senti = 0
                        numWords = len(parts)/3 - 1
                        i = 1

                        while i <= numWords:
                            senti += (float(parts[3*i+1]) + float(parts[3*i+2]))/2
                            i += 1

                        sentiment[1] += numWords
                        sentiment[0] += senti
                                           
        return sentiment[0]/sentiment[1] #persons, organizations, locations, sentiment[0]/sentiment[1], personPairs
        
    except:
        print(sys.exc_info())
        return 


def extractDailyInfo(year, month, day):
    """
    Wrapper for extractInfo( )\n
    Return persons, organizations, personPairs, locations, sentiment/len(filePathList)
    """

    dirPath = "./data/{}-{}-{}*".format(year, month, day) # To be changed/ Hierarchy Structure
    
    filePathList = glob.glob(dirPath) 
    
    persons = dict()
    locations = dict()
    organizations = dict()
    personPairs = dict()
    sentiment = 0
    
    for filePath in filePathList:
        try:
            sentiment += extractInfo(filePath, persons, locations, organizations, personPairs)
        except: # If the script isn't written in English
            pass
    
    # Sort the dictionaries, result in a sorted list containing key-value tuples [(<key>,<value>),...]
    persons = sorted(persons.items(), key=lambda item:item[1], reverse=True)
    locations = sorted(locations.items(), key=lambda item:item[1], reverse=True)
    organizations = sorted(organizations.items(), key=lambda item:item[1], reverse=True)
    personPairs = sorted(personPairs.items(), key=lambda item:item[1], reverse=True)

    personPairs1 = dict() # for network
    personPairs2 = dict() # for heatmap, only take 22 persons

    personList = []
    for pair in personPairs:
        if pair[1] > 3:
            personPairs1[pair[0]] = pair[1]
        if len(personList) < 22:
            personPairs2[pair[0]] = pair[1]
            if pair[0][0] not in personList:
                personList.append(pair[0][0])
            if pair[0][1] not in personList:
                personList.append(pair[0][1])

    return persons, organizations, personPairs1, personList, personPairs2, locations, sentiment/len(filePathList)


