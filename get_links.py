import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
import sys
import cv2
import shutil
import urllib.request
import numpy as np
from get_images import *
import random
import time

#get the links to each of the product images then run the get images function
def get_links(URL, referer, directory,image_grab = True):
    
    startTime=time.time()
    proxiesFile=open('proxies.txt','r')
    proxies=proxiesFile.readlines()
    proxiesFile.close()
    n=0
    username=[]
    password=[]

    for line in range(len(proxies)):
        temp=proxies[line].split(':')
        username.append(temp[0])
        password.append(temp[1])

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    headers = {'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)], 'referer': referer}
    proxies={"http":"proxy.homeip.io:1025"}
    auth=HTTPProxyAuth(username[random.randint(0,len(username)-1)],password[random.randint(0,len(password)-1)])
    r=requests.get(URL,headers=headers,proxies=proxies,auth=auth)


    soup=BeautifulSoup(r.content,'html5lib')
    links=[]
    i=0

    #find the image links from the href html tag
    for img in soup.select('a[href] img'):
        link=img.find_parent('a',href=True)
        links.append(link['href'])
        

    with open('href_urls.txt','w') as f:
        sys.stdout=f
        print(links)

    sys.stdout=sys.__stdout__

    titleURL=soup.find('title')
    if image_grab==True:
        
        for j in range(len(links)-2):

           if links[j+2].find(r'/gp/')==-1 and links[j+2].find(r'https:')==-1 and links[j+2].find('javascript:void')==-1:
                newURL=r'https://www.amazon.com' + links[j+2]

                a=0

                headers = {'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]}


                if a<len(username)-1:
                    get_images(newURL,URL,directory) 
                    a=a+1
                else:
                    a=0
                    get_images(newURL,URL,directory)



    return

