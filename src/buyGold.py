import requests
import requests.auth
import re
def buy_gold(user, key):
  try:
		re1='(t)'	# Any Single Word Character (Not Whitespace) 1
		re2='(\\d+)'	# Integer Number 1
		re3='(_)'	# Any Single Character 1
		rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
		m = rg.search(user)
		#Distinguishes between users and comments/submissions
		if m:
			params = {"fullname": user}
			headers = {"Authorization": "bearer " + str(key) + "", "User-Agent": "gold giving bot"}
			response = requests.post("https://oauth.reddit.com/api/v1/gold/gild/fullname", headers=headers, params=params)
			return "success"
		else:
			params = {"months": 1, "username": user}
			headers = {"Authorization": "bearer " + str(key) + "", "User-Agent": "gold giving bot"}
			response = requests.post("https://oauth.reddit.com/api/v1/gold/give/username", headers=headers, params=params)
			return "success"
	except:
		return "error"
