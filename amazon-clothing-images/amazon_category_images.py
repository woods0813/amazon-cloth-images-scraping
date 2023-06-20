from get_links import *
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

run=True
##Set up directories in which to place the images
baseDirectory=r'C:\Users\tbrad\AppData\Local\Programs\Python\Python37\Image_Scraping_Tests'
subDirectories=[r'Womens\Coats & Jackets',  r'Womens\Dresses', r'Womens\Suiting & Blazers',r'Womens\Sweaters', r'Womens\Tops & Tees',] 
num_images=[None]*len(subDirectories)

if __name__ =='__main__':
    ##primary function which uses multi-threading and run's through a given list of URL's (the amazon category pages) and uses the other functions to extract necessary images
    init_start_time = time.time()
    def main(URLlist,list_num):
        directory=baseDirectory+'\\'+subDirectories[list_num]
        threads=[]
        with ProcessPoolExecutor(max_workers=5) as executor:
            for n in range(1,len(URLlist)):
                threads.append(executor.submit(get_links,URLlist[n],URLlist[n-1],directory))
                
    ##creates the necessary list of urls and runs the primary function
    while run:
        coats_and_jackets_urls=[]
        suiting_and_blazers_urls=[]
        sweaters_urls=[]
        tops_and_tees_urls=[]
        dresses_urls = []
        suiting_and_blazers_urls = []

        ##starts at a random page between 0 (1) to 299 (300) and adds a list of the following 100 pages' urls for each category
        starting_num=1

        for i in range(starting_num,starting_num+300):
            coats_and_jackets_urls.append(r'https://www.amazon.com/s?i=fashion-womens-clothing&rh=n%3A1044646&fs=true&page='+str(i+1)+'&qid=1649890112')
            suiting_and_blazers_urls.append(r'https://www.amazon.com/s?i=fashion-womens-clothing&rh=n%3A9522932011&fs=true&page='+str(i+1)+'&qid=1649890440')
            sweaters_urls.append(r'https://www.amazon.com/s?i=fashion-womens-clothing&rh=n%3A1044456&fs=true&page='+str(i+1)+'&qid=1649890288')
            tops_and_tees_urls.append(r'https://www.amazon.com/s?i=fashion-womens-clothing&rh=n%3A2368343011&fs=true&page='+str(i+1)+'&qid=1649890486')
            dresses_urls.append(r'https://www.amazon.com/s?i=fashion-womens-clothing&rh=n%3A1045024&fs=true&page=' + str(i+1) + '&qid=1687210418')

        clothing_urls=[coats_and_jackets_urls, dresses_urls, suiting_and_blazers_urls, sweaters_urls, tops_and_tees_urls]

        ##run the primary function for each category
        for i in range(len(clothing_urls)):
            startTime=time.time()
            main(clothing_urls[i],i)
            num_images[i]=len(os.listdir(baseDirectory+'\\'+subDirectories[i]))
            time.sleep(1)
            print('Time of operation: ', time.time()-startTime)

        ##stop if the number of images for a given category exceeds 10000
        print(num_images)
        for i in range(len(num_images)):
            if num_images[i]>=10000:
                run=False

    print('total time to get images: ', time.time() - init_start_time)
