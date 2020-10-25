from time import sleep
import random
from selenium.webdriver.common.keys import Keys
import re

def getReviewUrl(movieId):
    '''
    Returns the review page URL from a movie id
    '''
    return "https://www.imdb.com/title/{0}/reviews".format(movieId)

def getSortType(reviewOptions):
    return reviewOptions['sort_by']
    
def getSortOrder(reviewOptions):
    return reviewOptions['sort_order']

def getMaxReviews(reviewOptions):
    return reviewOptions['max_reviews']

def getReviews(driver, movieId, reviewOptions):
    '''
    Scraps the reviews from the given movie (movieId)
    '''
    sortType = getSortType(reviewOptions)
    sortOrder = getSortOrder(reviewOptions)
    maxReviews = getMaxReviews(reviewOptions)

    review_page = getReviewUrl(movieId)
    driver.get(review_page)
    
    reviews_ret = []
    # TODO Scrap the content of the website and return a list of dictionaries with the same structure as getReviewsStub
    #Comptem el número d'elements de la pàgina:
    reviews = driver.find_elements_by_xpath('//div[contains(@class,"imdb-user-review")]')
    print (len(reviews))
    max = maxReviews
    print (max)
    while len(reviews) < max:
        boto = driver.find_element_by_xpath('//button[@id="load-more-trigger"]')
        try:
            boto.click()
            sleep(random.uniform(8.0,10.0))
            reviews = driver.find_elements_by_xpath('//div[contains(@class,"imdb-user-review")]')
        except:
            break
   
    recorregut = 1
    for i in range(max):
        rating = None
        rating_ok = None
        try:
            rating = driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//div[contains(@class, "ratings")]'.format(i+1)).text
            match = re.search(r'(\d+)/10', rating)
            if (match):
                rating_ok = match.group(1)
        except Exception as e:
            pass
        print(rating_ok)
        #print(rating)
        
        titulo = driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//a[@class="title"]'.format(i+1)).text
        print(titulo)
        
        username= driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//span[@class="display-name-link"]'.format(i+1)).text
        print(username)
        
        date = driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//span[@class="review-date"]'.format(i+1)).text
        print(date)
        pos_1 = date.index(' ')
        dia=date[0:pos_1]
        mesos = 1
        mes="/00/"
        while mesos < 13:
            if "January" in date:
                mes="/01/"
                break
            elif "February" in date:
                mes="/02/"
                break
            elif "March" in date:
                mes="/03/"
                break
            elif "April" in date:
                mes="/04/"
                break
            elif "May" in date:
                mes="/05/"
                break
            elif "June" in date:
                mes="/06/"
                break
            elif "July" in date:
                mes="/07/"
                break
            elif "August" in date:
                mes="/08/"
                break
            elif "September" in date:
                mes="/09/"
                break
            elif "October" in date:
                mes="/10/"
                break
            elif "November" in date:
                mes="/11/"
                break
            elif "December" in date:
                mes="/12/"
                break
            else:
                mesos = mesos + 1
        any=date[-4:]
        data = dia + mes + any
        print(data)
        
        comentari = driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//div[contains(@class, "show-more")]'.format(i+1)).text
        comentari = re.sub(r'\s+',' ', comentari)
        print(comentari)
        
        helpful = driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//div[contains(@class, "actions")]'.format(i+1)).text
        match = re.search(r'(\d+) out of (\d+) found this helpful\.', helpful)
        helpfulYes = None
        helpfulTotal = None
        if (match):
            helpfulYes = match.group(1)
            helpfulTotal = match.group(2)
        print(helpfulYes, helpfulTotal)

        isSpoiler = False
        try:
            spoiler= driver.find_element_by_xpath('(//div[contains(@class,"imdb-user-review")])[position()={0}]//span[(@class="spoiler-warning")]'.format(i+1)).text
            isSpoiler = True
        except Exception as e:
            pass
        print(isSpoiler)
        
        recorregut = recorregut + 1
        print(recorregut)
        if len(reviews) < max:
            max = len(reviews)
            print(max)
    #test mode 2 per guardar csv
    
        reviews_ret = reviews_ret + [{
            'movieId': movieId,
            'username':username,
            'date':data,
            'review_title':titulo,
            'rating':rating_ok,
            'text':comentari,
            'helpfulYes':helpfulYes,
            'helpfulTotal':helpfulTotal,
            'isSpoiler': isSpoiler
        }]
    # END
    return reviews_ret

def getReviewsStub(driver, movieId, reviewOptions):
    '''
    Returns an example list of reviews
    '''
    return [
        {
            'movieId': movieId,
            'username':'kath',
            'date':'2020-05-13',
            'review_title':'amaziing movie',
            'rating':10,
            'text':'i believe this movie is pretty good',
            'helpfulYes':180,
            'helpfulTotal':200,
            'isSpoiler':True
        },
        {
            'movieId': movieId,
            'username':'marie',
            'date':'2020-02-13',
            'review_title':'interesting movie',
            'rating':7,
            'text':'kinda ok i believe',
            'helpfulYes':20,
            'helpfulTotal':500,
            'isSpoiler':False
        }
    ]
    
def getMoviesReviewsStub(driver, moviesIds, reviewOptions):
    reviews = []
    for movieId in moviesIds:
        reviews = reviews + getReviewsStub(driver, movieId, reviewOptions)
    return reviews

def getMoviesReviews(driver, moviesIds, reviewOptions):
    reviews = []
    for movieId in moviesIds:
        reviews = reviews + getReviews(driver, movieId, reviewOptions)
    return reviews
    