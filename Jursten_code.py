#!/usr/bin/env python
# import library
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import instaloader
from instaloader import Instaloader, Profile
import random
import time
import csv,json

# source Code
class Login:
	def __init__(self,login_user,password,user):
		# username
		self.login_user = login_user
		# password
		self.password = password
		# scraped username
		self.user = user 

	# Information function
	def Information(self):
		print('----------------')
		# scraped trae id dynamically
		try:
			links = "http://beta.scouted.by/v1/exportDeepScouting?id=d0dd6e0cf620541fdd14527cc9a9813a&signature=6jNUs1R47zOMaW8goYDxIa5XIzA="
			f = requests.get(links)
			print(json.loads(f.text)['trace_id'])
			Trace_id = json.loads(f.text)['trace_id']
			print('Try trace id-------------',Trace_id)
		except:
			Trace_id = '6177d265421aa9234b8c6998'
			print('except:-------------',Trace_id)

		accounts = [('mikalouisa2','kp48ffkn'),('louisamika2','kp48ffkn'),('LianneStaps9','kp48ffkn')]
		random.shuffle(accounts)
		Insta_user = accounts[0][0]
		print("user:--",Insta_user)
		link = 'https://www.instagram.com/accounts/login/'
		login_url = 'https://www.instagram.com/accounts/login/ajax/'
		times = int(datetime.now().timestamp())

		payload = {
			'username': 'LianneStaps9',
			'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{times}:kp48ffkn',  # <-- note the '0' - that means we want to use plain passwords
			'queryParams': {},
			'optIntoOneTap': 'false'
		}

		with requests.Session() as s:
			r = s.get(link)
			csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
			r = s.post(login_url,data=payload,headers={
				"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
				"x-requested-with": "XMLHttpRequest",
				"referer": "https://www.instagram.com/accounts/login/",
				"x-csrftoken":csrf
			})
			print(r.json())

		# Instagram Login 
		loader = Instaloader()
		try:
			loader.login(self.login_user, self.password)
		except:
			# wrong username and password or block user
			print('Cannot Login')

		# Scraped username is stored in user list_of_user.
		list_of_user = []

		for users in self.user:
			print(users)
			#sent the username to fetching the information of the user.
			profile = Profile.from_username(loader.context, users)
			# Scraped Following of the user.
			followings = profile.get_followees()
			# Scraped followers of the user.
			followers = profile.get_followers()
			
			# Stored Scraped following username in list.
			for following in followings:
				if following not in list_of_user:
					print(following.username)
					list_of_user.append(following.username)
					row = [following.username]
					
			# Stored fethed follower username in list
			for follower in followers:
				if follower not in list_of_user:
					print(follower.username)
					list_of_user.append(follower.username)
					row = [follower.username]


			# Get information 
			def Get_info(list_of_user):
				# Scraped user deatil one by one.
				for user_name in list_of_user:
					Photo3 = []
					try:
						print("New user:-----------------",user_name)
						data = s.get('https://www.instagram.com/'+str(user_name)+'/?__a=1')
						details = json.loads(data.text)['graphql']['user']
						# User rofile description
						description = details['biography']
						# User followers count
						followers = details['edge_followed_by']['count']
						# User following count
						Following = details['edge_follow']['count']
						# User profile picture
						profile_pic = details['profile_pic_url_hd'].replace('?','----').replace('&','____')

						display_url = details['edge_owner_to_timeline_media']['edges']
						print(description,followers,Following,profile_pic)
						# User +3 Photos 
						photo3 = []
						count = 0
						for i in display_url:
							photo3.append(i['node']['display_url'].replace('?','----').replace('&','____').strip())
							print(i['node']['display_url'])
							count = count + 1
							if count == 4:
								print('Loop Break')
								break
						try:
							file_1 = photo3[0]
						except:
							file_1 = ''
						try:
							file_2 = photo3[1]
						except:
							file_2 = ''
						try:
							file_3 = photo3[2]
						except:
							file_3 = ''
						try:
							file_4 = photo3[3]
						except:
							file_4 = ''
						# Stored data in the database using an Api "https://beta.scouted.by/v1/importDeepScouting"
						Url = "https://beta.scouted.by/v1/insertDeepScouting?id=d0dd6e0cf620541fdd14527cc9a9813a&signature=d0dd6e0cf620541fdd14527cc9a9813a-"+str(Trace_id)+'-'+str(user_name)+'-'+"02a21adad3229c35f5bfc20ecbbb9ae1&followers="+str(followers)+"&following="+str(Following)+"&profile_photo="+str(profile_pic)+"&blocked=0&description="+str(description)+"&photos[]="+str(file_1)+"&photos[]="+str(file_2)+"&photos[]="+str(file_3)+"&photos[]="+str(file_4)+"=&trace_id="+str(Trace_id)+"&instagram="+str(user_name)                            
						f = requests.get(Url)
						print(f.text)
						print('Done')
					except:
						print("nooooooooooooooooooooooo")
						pass

			# Get_info function call
			Get_info(list_of_user)

# instagram account list
account = [('scout_marie1','na888888'),('irissannevloik','kp48ffkn'),('polinakurtaa','kp48ffkn')]
random.shuffle(account) 
Insta_users = account[0][0]
Insta_password = account[0][1]
# users list
scraped_user = []
with open('scoutinglist - Blad.csv', 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		scraped_user.append(row[0])
Username = Login('LianneStaps9','kp48ffkn',scraped_user)
Username.Information()





