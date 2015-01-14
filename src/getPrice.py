import requests
import requests.auth
import time
import json

def getPrices():
        print "Grabbing price..."
        dogeprice = parsePrices("doge")
        btcprice = parsePrices("btc")
        ltcprice = parsePrices("ltc")
        rddprice = parsePrices("rdd")
        obj3 = open('price.txt', 'w')
        obj3.write(str(dogeprice) + "\n" + str(btcprice) + '\n' + str(ltcprice) + '\n' + str(rddprice))
        obj3.close()
        print 'Done'
def parsePrices(currency):
        code = requests.get('http://coinmarketcap.northpole.ro/api/' + currency + '.json')
        json_input = code.json()
        decoded = json.dumps(json_input)
        decoded = json.loads(decoded)
        price = decoded['price']
        price = float(price)
        price = 1.3 * 4 / price 
        price = round(price,7)
        return price
while True:
    getPrices()
    for x in range(2700,-1,-1):
        print x
        x+=1
        time.sleep(1)
