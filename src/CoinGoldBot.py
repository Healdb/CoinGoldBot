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
import helpers
import fileHelpers

username,password,apikey1,apikey2 = helpers.getSensitive()
r = praw.Reddit('Coin Gold Bot')
r.login(username,password)
tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)
pattern = re.compile('\+/u/coingoldbot\s+(\w+)', re.IGNORECASE)
exchange = Api(apikey1, apikey2)

def find_summons():
    global key
    #Searches for summoning command
    messages = r.get_unread('mentions')
    time.sleep(3)
    for comment in messages:
        print 'looking for summons'
        comment_text,origin_comment, op_name, link_id = helpers.commentParser(comment)
        time.sleep(2)
        matches = pattern.findall(comment_text)
        if matches:
            print 'Found comment!'
            username = helpers.usernameParser(matches)
            gild = 'gild'
            try:
                currencyID, price, currencyName = helpers.detectCurrency(comment_text)
            except:
                helpers.respondUnsupported(origin_comment)
                break
            address = helpers.genNewAddress(currencyID)
            if username == gild:
                helpers.respondGild(op_name,link_id,address,price,origin_comment,currencyName)
                break
            else:
                helpers.respondUser(op_name,link_id,address,price,origin_comment,username,currencyName)
                break
def responses():
    global key
    print 'Done. Starting second part' 
    time.sleep(5)
    f =open('address.txt')
    lines=f.readlines()
    for line in lines:
        try:
           user, currentAddress = line.split(",")
        except ValueError:
           print 'Empty File'
           break
        currentAddress = currentAddress.rstrip()
        if helpers.checkAddress(user, currentAddress):
            print 'Buying gold...'
            recieverDict = fileHelpers.readDict("links.txt")
            reciever = recieverDict[str(currentAddress)]
            check = "success"
            #check = buyGold.buy_gold(reciever, key)
            if check == "success":
                pricesDict = fileHelpers.readDict('userPrice.txt')
                print pricesDict                               
                userPrice = pricesDict[currentAddress]
                words1 = [user + "," + currentAddress]
                words2 = [currentAddress + "," + reciever]
                words3 = [currentAddress + "," + userPrice]
                fileHelpers.delete_line(words1, 'address')
                fileHelpers.delete_line(words2, 'links')
                fileHelpers.delete_line(words3, 'userPrice')
                print "FINISHED"
                r.send_message(user, 'Thank you for using me!', 'Congrats! You have just sent a month of gold to a cool user. Thank you for using me!')
            else:
                print 'ERROR, problem with buying gold'
while True:
    keyFile = open('access_key.txt', 'r')
    key = keyFile.read()
    print "Start"
    find_summons()
    responses()
    time.sleep(10)
