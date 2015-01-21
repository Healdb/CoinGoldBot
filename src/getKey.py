import requests
import requests.auth
import time
import json
import helpers

username,password,trash1,trash2,reddit1,reddit2 = helpers.getSensitive()

def get_key():
    print "grabbing key..."
    try:
        client_auth = requests.auth.HTTPBasicAuth(reddit1, reddit2)
        post_data = {"grant_type": "password", "username": username, "password": password}
        response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)
        json_input = response.json()
        decoded = json.dumps(json_input)
        decoded = json.loads(decoded)
        price = decoded['access_token']
        obj3 = open('access_key.txt', 'w')
        obj3.write(price)
        obj3.close()
        print 'Done'
    except:
        time.sleep(3)
        get_key()
        
while True:
    get_key()
    for x in range(2700,-1,-1):
        print x
        x+=1
        time.sleep(1)
