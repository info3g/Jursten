#!/usr/bin/env python

# import library
from selenium.webdriver.chrome.options import Options
from instaloader import Instaloader, Profile
from selenium import webdriver
import random
import time
import csv

# Source Code
class Login:
    def __init__(self, loin_user, pasword, user):
        # Username
        self.loin_user = loin_user
        # Password
        self.pasword = pasword
        # Scraped username
        self.user = user

    # Information function
    def Infomation(self):
        # Open chrome web browser and headless
        options = Options()
        options.headless = True
        # driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)

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
                        print("New user:--------------",user_name)
                        profile = Profile.from_username(loader.context, user_name)
                        # User profile picture
                        print('profile_pic_url_hd',profile.__dict__['_node']['profile_pic_url_hd'].replace('?','----').replace('&','____'))
                        profile_pic = profile.__dict__['_node']['profile_pic_url_hd'].replace('?','----').replace('&','____')
                        # User followers count
                        print('followers',profile.__dict__['_node']['edge_followed_by']['count'])
                        followers = profile.__dict__['_node']['edge_followed_by']['count']
                        # User following count
                        print('Following',profile.__dict__['_node']['edge_follow']['count'])
                        Following = profile.__dict__['_node']['edge_follow']['count']
                        # User rofile description
                        print('description',profile.__dict__['_node']['biography'])
                        description = profile.__dict__['_node']['biography']
                        # User +3 Photos
                        count = 0
                        post = profile.__dict__['_node']['edge_owner_to_timeline_media']['edges']
                        for i in post:
                            Photo3.append(i['node']['display_url'].replace('?','----').replace('&','____').strip())
                            print(i['node']['display_url'].replace('?','----').replace('&','____'))
                            count = count+1
                            if count == 4:
                                print("Loop Break")
                                break
                        # Stored data in the database using an Api "https://beta.scouted.by/v1/importDeepScouting"
                        try:
                            if len(Photo3) == 0:
                                print('If Condition Private User')
                                urls = ''
                            else:
                                print("Else Condition 4+ photos")
                                try:
                                    url = Photo3[0]
                                except:
                                    url = ''
                                try:
                                    url_ = Photo3[1]
                                except:
                                    url_ = ''
                                try:   
                                    url_s = Photo3[2]
                                except:
                                    url_s = ''
                                try:
                                    url_post = Photo3[3]
                                except:
                                    url_post = ''
                                urls = str(url)+','+str(url_)+','+url_s+','+url_post
                                print(urls)
                            Trace_id = '6177d265421aa9234b8c6998'
                            Url = "https://beta.scouted.by/v1/insertDeepScouting?id=d0dd6e0cf620541fdd14527cc9a9813a&signature=d0dd6e0cf620541fdd14527cc9a9813a-"+str(Trace_id)+'-'+str(user_name)+'-'+"02a21adad3229c35f5bfc20ecbbb9ae1&followers="+str(followers)+"&following="+str(Following)+"&profile_photo="+str(profile_pic)+"&blocked=0&description="+str(description)+"&photos[]="+urls+"=&trace_id="+str(Trace_id)+"&instagram="+str(user_name)
                            driver.get(Url)
                        except:
                            pass
                    except:
                        pass
                    time.sleep(20)
           
            # Get_info function call        
            Get_info(list_of_user)
           
# instagram account list
account = [('scout_marie1','na888888'),('scout_marie2','na888888'),('scout_marie3','na888888')]
random.shuffle(account)    
Insta_user = account[0][0]
Insta_password = account[0][1]
# users list
scraped_user = []
with open('scoutinglist - Blad.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        scraped_user.append(row[0])
Username = Login(Insta_user,Insta_password, scraped_user)
Username.Infomation()
