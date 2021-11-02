#!/usr/bin/env python

# import library
from instaloader import Instaloader, Profile
from selenium import webdriver
import random
import time
import csv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import json
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Source Code
class Login:
    def __init__(self, loin_user, pasword, user):

        # Username
        self.loin_user = loin_user
        # Password
        self.pasword = pasword
        # Scraped username
        self.user = user
        print(self.user)
    # Information function
    def Infomation(self):
        print("-----------------")
        # Scraped Trace Id dynamically
        try:
            link = 'https://beta.scouted.by/v1/exportDeepScouting?id=d0dd6e0cf620541fdd14527cc9a9813a&signature=6jNUs1R47zOMaW8goYDxIa5XIzA='
            f = requests.get(link)
            print(json.loads(f.text)['trace_id'])
            Trace_id = json.loads(f.text)['trace_id']
            print('try Trace_id:-----------------------',Trace_id)
        except:
            Trace_id = '617a5261421aa9600f98d65d'
            print('except:------------',Trace_id)

        accounts = [('mikalouisa2','kp48ffkn'),('LianneStaps9','kp48ffkn'),('louisamika2','kp48ffkn')]
        random.shuffle(account)    
        Insta_user = accounts[0][0]
        print('Insta_user:------',Insta_user)
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        payload = {
            'username': Insta_user,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:kp48ffkn',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        with requests.Session() as s:
            r = s.get(link)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
            r = s.post(login_url, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            })
            print(r.json())




        # Instagram Login
        loader = Instaloader()
        try:
            loader.login(self.loin_user, self.pasword)
            # Login
        except:
            # Wrong username Password or block user account
            print('cannot login')
            
        # Scraped username is stored in user list_of_user.
        list_of_user = []
        print("***********")
        for users in self.user:
            time.sleep(10)
            print('users:---------------',users)
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
                    time.sleep(0.30)
                    list_of_user.append(following.username)
                    row = [following.username]
                    
            # Stored fethed follower username in list
            for follower in followers:
                if follower not in list_of_user:
                    print(follower.username)
                    time.sleep(0.30)
                    list_of_user.append(follower.username)
                    row = [follower.username]
            
            # Get information 
            def Get_info(list_of_user):
                # Scraped user deatil one by one.
                test = []
                for user_name in list_of_user:
                    try:
                        print("New user:--------------",user_name)
                        data = s.get('https://www.instagram.com/'+str(user_name)+'/?__a=1')
                        time.sleep(8)
                        details = json.loads(data.text)['graphql']['user']
                        # User rofile description
                        time.sleep(1)
                        description = details['biography']
                        # User followers count
                        time.sleep(1)
                        followers = details['edge_followed_by']['count']
                        # User Following count
                        time.sleep(1)
                        Following = details['edge_follow']['count']
                        # User profile picture
                        time.sleep(1)
                        profile_pic = details['profile_pic_url_hd'].replace('?','----').replace('&','____')
                        time.sleep(1)
                        display_url = details['edge_owner_to_timeline_media']['edges']
                        print(description,followers,Following,profile_pic)
                        # User +3 Photos
                        photo3 = []
                        count = 0
                        for i in display_url:
                            photo3.append(i['node']['display_url'].replace('?','----').replace('&','____'))
                            print(i['node']['display_url'])
                            count = count + 1
                            test.append(count)
                            if count == 4:
                                print("Loop Break")
                                break
                        time.sleep(1)
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

                        Url = "https://beta.scouted.by/v1/insertDeepScouting?id=d0dd6e0cf620541fdd14527cc9a9813a&signature=d0dd6e0cf620541fdd14527cc9a9813a-"+str(Trace_id)+'-'+str(user_name)+'-'+"02a21adad3229c35f5bfc20ecbbb9ae1&followers="+str(followers)+"&following="+str(Following)+"&profile_photo="+str(profile_pic)+"&blocked=0&description="+str(description)+"&photos[]="+str(file_1)+"&photos[]="+str(file_2)+"&photos[]="+str(file_3)+"&photos[]="+str(file_4)+"=&trace_id="+str(Trace_id)+"&instagram="+str(user_name)
                        f = requests.get(Url)
                        print(f.text)
                        print("Done")
                    except:
                        pass
                    
                    if len(test) == 160 or len(test) == '100':
                        time.sleep(2000)
                    time.sleep(100)
            # Get_info function call        
            Get_info(list_of_user)
           

# instagram account list
account = [('scout_marie1','na888888'),('john20.21','puneet@6644'),('irissannevloik','kp48ffkn'),('polinakurtaa','kp48ffkn')]
random.shuffle(account)    
Insta_user = account[0][0]
Insta_password = account[0][1]
# users list
scraped_users = []
with open('scoutinglist - Blad.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        scraped_users.append(row[0])
Username = Login(Insta_user,Insta_password, scraped_users)
Username.Infomation()




