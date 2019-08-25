#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The algorithm is still not good enough.
"""

import wikipedia
import spacy
import nltk.data

import string
import re

import stopwords

# The two NLP models will only be loaded once
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
nlp = spacy.load('en_core_web_md')

def getOccupations(name):
    """
    Return a list of occupations (~~and nationality~~) of a certain person via the wikipedia API   
    """
    try:
        # {ppl} <is a> {title} <prep> <,who>
        line = tokenizer.tokenize(wikipedia.summary(name,sentences=5))[0]
        startSign = ["is an", "was an", "was a", "is a", "is"] # Strict order: an before a, or there will be 'n' lefted

        # Get the part after startSign
        for i in startSign:
            if len(line.split(i)) > 1:
                line = line.split(i)[1]
                break

        # Start to get nationality and job titles
        line = line.split('who')[0]
        line = line.strip(', ')

        nation = []
        occupations = []

        # Start NLP
        doc = nlp(line)

        for ent in doc.ents:
            if ent.label_ == 'NORP' or ent.label_ == 'GPE':
                nation.append(ent.text)

        # Get rid of the nationality    
        words = line.split(' ', maxsplit=1)
        if words[0] in nation:
            line = line.split(' ',maxsplit=1)[1] 

        # if len(line.split('from'))>1:
        #     line = line.split('from')[0]

        # Start to take the occupations
        for occupation in line.split(','):
            occupation = occupation.strip(' ')

            if len(occupation.split('and'))>1:
                for elem in occupation.split('and'):
                    if elem != '' and elem != ' ':
                        occ = stripAdj(elem.strip())
                        occ = occ.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
                        occ = re.sub(r'[0-9]+', '', occ) # remove number
                        if occ not in stopwords.stopwords:
                            occupations.append(occ)

            else:
                occupation = occupation.translate(str.maketrans('', '', string.punctuation))
                occupation = occupation.translate(str.maketrans('', '', string.digits))
                if occupation not in stopwords.stopwords:
                    occupations.append(stripAdj(occupation))
                
        return occupations
    
    except: # person not found
        return ' '


def stripAdj(phrase):
    """
    Assume that spaCy has been imported and nlp model has been loaded\n
    tokenizer and nlp object will be created in main to avoid repetitive loading (?necessary?) 
    """
    
    # if len(phrase.split())==1:
    #     return phrase
    
    newPhrase = []
    doc = nlp(phrase)
    for token in doc:
        if token.pos_ == 'NOUN':
            newPhrase.append(token.text)
    
    finalPhrase = ''
    for word in newPhrase:
        finalPhrase += word + ' '
        
    return finalPhrase.strip()


def getDailyOccupations(nameList, year, month, day):
    """
    Wrapper for getOccupations\n
    Return sorted list of occupation counts
    """

    result = dict()

    num = 50
    if len(nameList) < 50:
        num = len(nameList)

    for i in range(num):
        name = nameList[i]
        for occupation in getOccupations(name):
            if occupation == ' ' or occupation == '':
                continue
            elif occupation in result:
                result[occupation] += 1
            else:
                result[occupation] = 1

    return sorted(result.items(), key=lambda item:item[1], reverse=True)

    
