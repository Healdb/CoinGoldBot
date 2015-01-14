#coding: utf-8
import time
import requests
import buyGold
from Cryptsy import Api
import praw
import re
import os
import csv
import requests
import requests.auth
import json
import urllib2
import fileHelpers

def getSensitive():
    f=open("config.txt")
    lines=f.readlines()
    trash, username = lines[0].split(":")
    trash, password = lines[1].split(":")
    trash, apikey1 = lines[2].split(":")
    trash, apikey2 = lines[3].split(":")
    return username.rstrip(), password.rstrip(), apikey1.rstrip(),apikey2.rstrip()

username,password,apikey1, apikey2 = getSensitive()
r = praw.Reddit('Coin Gold Bot')
r.login(username,password)
exchange = Api(apikey1, apikey2)

def getPrice(com_id,com_permlink):
    submission = r.get_submission(url=com_permlink + com_id)
    submission = submission.comments
    for comment in submission:
        com_id =  comment.id
        oldstr = comment.permalink
        newstr = oldstr.replace(com_id, "")
        temp_id = comment.parent_id
        link_id = temp_id[3:]
        com_link = newstr + link_id
        submission = r.get_submission(url=com_link)
        submission = submission.comments
        for comment in submission:
            text = comment.body
            com_id =  comment.id
            oldstr = comment.permalink
            newstr = oldstr.replace(com_id, "")
            temp_id = comment.parent_id
            link_id = temp_id[3:]
            com_link = newstr + link_id
            submission = r.get_submission(url=com_link)
            submission = submission.comments
            for comment in submission:
                text = comment.body
                link = comment.permalink
                re1='.*?'	# Non-greedy match on filler
                re2='(\\d+)'	# Integer Number 1
                rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
                m = rg.search(text)
                if m:
                    int1=m.group(1)
                    return int1, link
def user_to_full(username):
    try:
        response = urllib2.urlopen('http://www.reddit.com/user/' + username + '/about.json')
        json_input = json.load(response)
        decoded = json.dumps(json_input)
        decoded = json.loads(decoded)
        name = decoded['data']['id']
        user_full = 't2_' + name
        return user_full
    except:
        print "Error: User does not exist"
        return 'user404failure'
def detectCurrency(text):
    f =open('price.txt')
    lines=f.readlines()
    re1='.*?'	# Non-greedy match on filler
    re2='(?:[a-z][a-z]+)'	# Uninteresting: word
    re3='.*?'	# Non-greedy match on filler
    re4='(?:[a-z][a-z]+)'	# Uninteresting: word
    re5='.*?'	# Non-greedy match on filler
    re6='((?:[a-z][a-z]+))'	# Word 1

    rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
    m = rg.search(text)
    if m:
        #Returns currency codes and predetermined price of the gold.
        word1=m.group(1)
        if word1 == 'DOGE':
            return 94, lines[0], 'DOGE'
        if word1 =="BTC":
            return 3, lines[1], "BTC"
        if word1 == "LTC":
            return 2, lines[2], "LTC"
        if word1 == "RDD":
            return 126, lines[3], "RDD"
        else:
            return 'ERROR'
def whichAddress(txt):
    if txt[0] == '1':
        return 'BTC'
    if txt[0] == 'L':
        return 'LTC'
    if txt[0] == 'R':
        return 'RDD'
    if txt[0] == 'D':
        return 'DOGE'
    else:
        print 'error'
def loadBalance(address):
    #print address
    currency = whichAddress(address)
    if currency == 'RDD':
        response = urllib2.urlopen('http://live.reddcoin.com/api/addr/' + str(address) + '/balance')
        json_input = json.load(response)
        decoded = json.dumps(json_input)
        decoded = json.loads(decoded)
        
        return decoded
    else:
        response = urllib2.urlopen('https://chain.so/api/v2/get_address_balance/' + currency + '/' + str(address))
        json_input = json.load(response)
        decoded = json.dumps(json_input)
        decoded = json.loads(decoded)
        name = decoded['data']['unconfirmed_balance']
        return name
def checkAddress(user, address):
    #print address
    pricesDict = fileHelpers.readDict('userPrice.txt')    
    userPrice = (pricesDict[address]).replace("\n", "")
    addressBalance = loadBalance(str(address))
    #print addressBalance
    #print 'hey'
    #print userPrice
    if userPrice == addressBalance:
        return True
    else:
        return False
def genNewAddress(id):
    x = exchange.generate_new_address(id)
    address = x['return']['address']
    return address
def commentParser(comment):
    author = comment.author
    return comment.body, comment, author.name, comment.parent_id
def respondUnsupported(origin_comment):
    origin_comment.mark_as_read()
    print 'Unsupported currency'
def respondGild(op_name,link_id,address,price,origin_comment,currencyName):
    dict1 = {address: link_id}
    dict2 = {op_name: address}
    dict3 = {address: str(price).rstrip()}
    fileHelpers.saveDict(dict1, "links.txt")
    fileHelpers.saveDict(dict2, "address.txt")
    fileHelpers.saveDict(dict3, "userPrice.txt")
    r.send_message(op_name, 'Hey', 'You are attempting to gild whatever object you have just commented on. Please send ' + price + ' ' + currencyName + ' to ' + str(address) + ' .')
    time.sleep(5)
    origin_comment.mark_as_read()
    print "Done"
def respondUser(op_name,link_id,address,price,origin_comment,username,currencyName):
    userf = user_to_full(username)
    if userf == 'user404failure':
        origin_comment.reply("I'm sorry, but that user does not seem to exist on reddit. Please try again")
        time.sleep(5)
        origin_comment.mark_as_read()
    else:
        r.send_message(op_name, 'Hey', 'You are attempting to buy a month of gold for /u/' + str(username) + '. Please send ' + str(price) + ' ' + currencyName + ' to ' + str(address) + ' .')
        dict1 = {address: userf}
        dict2 = {op_name: address}
        dict3 = {address: str(price).rstrip()}
        fileHelpers.saveDict(dict1, "links.txt")
        fileHelpers.saveDict(dict2, "address.txt")
        fileHelpers.saveDict(dict3, "userPrice.txt")
        time.sleep(5)
        origin_comment.mark_as_read()
        print "Done"
def usernameParser(matches):
    match = [str(healdb) for healdb in matches]
    username = ''.join(match)
    return username
