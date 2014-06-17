#python2
# -*- coding: utf-8 -*-

import facepy
import web, requests
import subprocess, threading
import os

def getAuthToken():
        '''Get client token by Client Authentication and Authorization'''
    
        app_id = '714940868529499'
        app_secret = '33bcfb01cdac919fe96266c762d5e16b'

        post_login_url = "http://0.0.0.0:8080/"
        url = ('/', 'index')
        
        global token
        
        #Webpy Handler Class                
        class index:
            def GET(self):
                user_data = web.input(code=None)
                code = user_data.code

                if not code:
                    dialog_url = ( "http://www.facebook.com/dialog/oauth?" +
                                   "client_id=" + app_id +
                                   "&redirect_uri=" + post_login_url +
                                   "&scope=read_mailbox" )

                    return "<script>top.location.href='" + dialog_url + "'</script>"
                else:
                    token_url = ( "https://graph.facebook.com/oauth/access_token?" +
                                  "client_id=" + app_id +
                                  "&redirect_uri=" + post_login_url +
                                  "&client_secret=" + app_secret +
                                  "&code=" + code )
                    response = requests.get(token_url).content

                    params = {}
                    result = response.split("&", 1)
                    for p in result:
                        (k,v) = p.split("=")
                        params[k] = v

                    access_token = params['access_token']  
                    
                    #Get extended token
                    global token
                    token = facepy.utils.get_extended_access_token(access_token, app_id, app_secret)[0]
                    
                    app.stop()
                    return "<script>window.close();</script>"
        
        #Start Web.py application in new thread and open Chromium            
        app = web.application(url, locals())
        th = threading.Thread(target=app.run)
        th.start()
        
        subprocess.Popen(['xdg-open', post_login_url])    
        th.join()
        
        return token
    

def getUnreadFBMessages(token):
        '''Get unread messages count from Facebook Inbox.'''
        
        query = 'SELECT unread_count FROM mailbox_folder WHERE folder_id=0'
        
        graph = facepy.GraphAPI(token)
        result = graph.fql(query)        
        count = result['data'][0]['unread_count']

        return count

def getUnreadMessages():
        '''Generates all login/token flux and gives back the message count.'''

        path = os.path.dirname(os.path.realpath(__file__))        
        f = open(os.path.realpath(path+'/token.cfg'), 'r')
        token = f.readline()
        f.close()
        
        try:
                n = getUnreadFBMessages(token)
                return int(n)
        except:
                token = getAuthToken()
                print(token)

                f = open('token.cfg', 'w')
                f.write(str(token))
                f.close()
                
                return -1
