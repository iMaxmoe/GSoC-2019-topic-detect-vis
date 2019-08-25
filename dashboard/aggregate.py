# -*- coding: utf-8 -*-

import json
from datetime import datetime

def aggregate(jsonFiles):

    new_doc, new_persons, new_links, new_nodes, new_axis, new_pairs, new_occupations = dict(), list(), list(), list(), list(), list(), list()
    persons, links, axis, pairs, occupations = dict(), dict(), list(), dict(), dict()

    # Do merge and accumulation for arrays
    for f in jsonFiles:   
        
        for p in f['persons']:
            if p['key'] in persons:
                persons[p['key']] += p['count']
            else:
                persons[p['key']] = p['count']
                
        for l in f['links']: # make sure there isn't double directed link
            if (l['source'], l['target']) in links:
                links[(l['source'], l['target'])] += l['value']
            elif (l['target'], l['source']) in links:
                links[(l['target'], l['source'])] += l['value']
            else:
                links[(l['source'], l['target'])] = l['value']
                
        for n in f['nodes']:
            if n not in new_nodes:
                new_nodes.append(n)
            
        for p in f['pairs']:
            if (p['source'], p['target']) in pairs:
                pairs[(p['source'], p['target'])] += p['value']
            elif (p['target'], p['source']) in pairs:
                pairs[(p['target'], p['source'])] += p['value']
            else:
                pairs[(p['source'], p['target'])] = p['value']
        
        for o in f['occupations']:
            if o['key'] in occupations:
                occupations[o['key']] += o['count']
            else:
                occupations[o['key']] = o['count']
                
    # Get axis from pairs
    pairs = sorted(pairs.items(), key=lambda item:item[1], reverse=True)
    count = 0

    for pair in pairs:
        if len(axis) < 22:
            count += 1
            p1, p2 = pair[0][0], pair[0][1]
            if p1 not in axis:
                axis.append(p1)
            if p2 not in axis:
                axis.append(p2)
        else:
            break
               
    pairs = pairs[:count]
                
    ## Generate aggregated JSON formatted file (document) from temporary dictionaries

    def truncate(array, maxlen):
        if len(array) > maxlen:
            array = array[:maxlen]
        return array

    #persons
    persons = sorted(persons.items(), key=lambda item:item[1], reverse=True)

    for person in persons:
        pair = { "key": person[0], "count": person[1] }
        new_persons.append(pair)
        
    new_doc['persons'] = truncate(new_persons, 50) # Do not need more than 50 persons for wordcloud

    #links: no need for sorting
    for link in links.items():
        link = { "source": link[0][0], "target": link[0][1], "value": link[1] }
        new_links.append(link)
        
    new_doc['links'] = new_links

    #nodes: simply used new_nodes, no need for re-constructing
    new_doc['nodes'] = new_nodes

    # axis
    new_doc['axis'] = axis

    #pairs: already sorted and truncated
    for pair in pairs:
        pair = { "source": pair[0][0], "target": pair[0][1], "value": pair[1] }
        new_pairs.append(pair)
        
    new_doc['pairs'] = new_pairs

    #occupations 
    occupations = sorted(occupations.items(), key=lambda item:item[1], reverse=True)

    for occ in occupations:
        pair = { "key": occ[0], "count": occ[1] }
        new_occupations.append(pair)
        
    new_doc['occupations'] = truncate(new_occupations, 50) # Do not need more than 50 occupations for wordcloud

    #last step
    jsonFile = json.dumps(new_doc)
    return jsonFile
    
    
def select(jsonFile):
    """
    Only take max=30 days & max=15 related persons
    """    
    doc, count, network = dict(), dict(), dict()
    new_count, new_network = list(), list()
    
    for c in jsonFile['count']:
        date, num = c['date'], c['num']
        date = date.strftime("%Y-%m-%d")
        count[date] = num
        
    for p in jsonFile['network']:
        name, num = p['name'], p['num']
        network[name] = num
        
    count = sorted(count.items(), key=lambda item:item[0]) #sort by date
    network = sorted(network.items(), key=lambda item:item[1], reverse=True)
    
    if len(count) > 30:
        count = count[-30:]
    
    if len(network) > 10:
        network = network[:15]
        
    for c in count:
        pair = { "date": c[0], "num": c[1] }
        new_count.append(pair)
        
    for n in network:
        pair = { "name": n[0], "num": n[1] }
        new_network.append(pair)
    
    doc['name'] = jsonFile['name']
    doc['count'] = new_count
    doc['network'] = new_network
    
    return json.dumps(doc)
    
    
def capitalize_name(name):
    parts = name.split(" ")
    if len(parts) > 1:
        name = ""
        for p in parts:
            p = p.lower().capitalize()
            name += p+' '
        return name[:-1]    
    else:
        return name
    
