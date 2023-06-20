import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
import sys
import cv2
import shutil
import urllib.request
import numpy as np
import time
import random
import os

#URL=r'https://www.amazon.com/b/?_encoding=UTF8&node=1045624&bbn=7141123011&ref_=Oct_d_odnav_d_2476517011_0&pd_rd_w=Luan1&pf_rd_p=0f6f8a08-29ea-497e-8cb4-0ccf91422740&pf_rd_r=7T8REXQ8PFEBN7Y64R06&pd_rd_r=ae033e84-af0b-4bd2-acd5-625a6c39a1db&pd_rd_wg=kDtz8'
#link_num=5

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

##Get the images from a specific product page. Takes in the URL of the actual product as well as the reference URL from which we got to this page, also the directory to place the image in
def get_images(URL,referrer,directory,txt_write=False):

    ##Set up proxies and user agents to be used
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]
    proxiesFile=open('proxies.txt','r')
    proxies=proxiesFile.readlines()
    proxiesFile.close()
    n=0
    username=[]
    password=[]
    directory_length=len(os.listdir(directory))

    for line in range(len(proxies)):
        temp=proxies[line].split(':')
        username.append(temp[0])
        password.append(temp[1])

    ##Make the request to the webpage
    proxy={"http":"proxy.homeip.io:1025"}
    time.sleep(random.random()*1)
    r=requests.get(URL,headers = {'Referrer': referrer ,'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]},proxies=proxy,auth=HTTPProxyAuth(username[random.randint(0,len(username)-1)],password[random.randint(0,len(password)-1)]))
    soup=BeautifulSoup(r.content,'html5lib')
    images=[]


    for image in soup.find_all('img'):
        images.append(image.get('src'))


    #print the list of image links to a file called image_urls (temporary)
    if txt_write==True:
        with open('image_urls.txt','w') as f:
            sys.stdout=f
            print(images)

    sys.stdout=sys.__stdout__
    imageArr=[]
    filename=str(directory.split('\\')[-1]+'.txt')
    
    ##Loop through images and obtain the correct image of the product and write it to the correct directory
    for j in range(len(images)-1):

        try:
            imgfilename=images[j].split('/')[-1]
        except:
            continue
        
        if imgfilename.find(r'_SX342_')!=-1:
            
            try:
                #time.sleep(random.random()*1)
                resp = requests.get(images[j],headers = {'Referrer': URL, 'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)]},proxies=proxy,auth=HTTPProxyAuth(username[random.randint(0,len(username)-1)],password[random.randint(0,len(password)-1)]),stream=True).raw
                imageArr = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(imageArr, cv2.IMREAD_COLOR)
                cv2.imwrite(directory+'\\'+imgfilename,image)
                new_length=len(os.listdir(directory))
                if new_length>directory_length:
                    break
                else:
                    continue
            except:
                print('not a static image')
        else:
            continue

    return
