from time import sleep
import random
import re
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import internal_find_element_by_xpath
from utils import obtainSingleElementFromText
from selenium.webdriver.support.select import Select

def getSortValueByOption(sortType):
    '''
    Returns the sort type as a query parameter from the configuration sort type
    '''
    if (sortType == 'helpfulness'):
        return 'helpfulnessScore'
    elif (sortType == 'date'):
        return 'submissionDate'
    elif (sortType == 'votes'):
        return 'totalVotes'
    elif (sortType == 'prolific'):
        return 'reviewVolume'
    elif (sortType == 'rating'):
        return 'userRating'
    return None

def getReviewUrl(movieId, sortType, sortOrder):
    '''
    Returns the review page URL from a movie id and the sort options
    '''
    return "https://www.imdb.com/title/{0}/reviews?sort={1}&dir={2}".format(movieId, getSortValueByOption(sortType), sortOrder)

def getSortType(reviewOptions):
    '''
    Gets the sort type from the configuration
    '''
    return reviewOptions['sort_by']
    
def getSortOrder(reviewOptions):
    '''
    Gets the sort order from the configuration
    '''
    return reviewOptions['sort_order']

def getMaxReviews(reviewOptions):
    '''
    Gets the max number of reviews to process per movie from the configuration
    '''
    return reviewOptions['max_reviews']
    
def getReviewFullXpath(pos, innerXPath):
    '''
    Gets the review XPath from the root element of the review webpage
    Each review is contained inside an imdb-user-review class div. 
    The position argument is used to determine which concrete review must be retrieved.
    The innerXPath parameter is concatenated to the review query in order to access the specific element inside the review
    '''
    fullXPath = '(//div[contains(@class,"imdb-user-review")])[position()={0}]{1}'.format(pos, innerXPath)
    return fullXPath
    
def getReviewAtPos(driver, pos, innerXPath):
    '''
    Gets the element inside the review container.
    The exact review is determined by the pos parameter
    The innerXPath parameter determines which element inside the review container must be retrieved
    '''
    return internal_find_element_by_xpath(driver, getReviewFullXpath(pos, innerXPath))
    
def getReviewTextAtPos(driver, pos, innerXPath):
    '''
    Obtains the text for an element inside a review container
    '''
    return getReviewAtPos(driver, pos, innerXPath).text

def getNumberReviewsLoaded(driver):
    '''
    Fetches the number of reviews currently loaded within the page
    '''
    return len(driver.find_elements_by_xpath('//div[contains(@class,"imdb-user-review")]'))
    
   
def getReviews(driver, movieId, reviewOptions):
    '''
    Scraps the reviews from the given movie (movieId)
    '''
    sortType = getSortType(reviewOptions)
    sortOrder = getSortOrder(reviewOptions)
    maxReviews = getMaxReviews(reviewOptions)

    
    review_page = getReviewUrl(movieId, sortType, sortOrder)
    print("Opening page: {0}".format(review_page))
    driver.get(review_page)    
    
    reviews_ret = []
    
    # Load pages until the number of elements is enough
    print("Determining if multiple pages must be loaded")
    boto = internal_find_element_by_xpath(driver, '//button[@id="load-more-trigger"]')
    
    while boto != None and boto.is_displayed() and getNumberReviewsLoaded(driver) < maxReviews:
        print("Needs more reviews. Attempting to load more reviews")
        boto.click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="lister"]//div[contains(@class,"ipl-load-more--loaded")]')))
        print("Load button clicked. Determining if more pages must be loaded...")
        boto = internal_find_element_by_xpath(driver, '//button[@id="load-more-trigger"]')
     
    # The pages are loaded. Determine the number of reviews to process.
    # If number of loaded reviews < max specified number then we proceed with the whole set of page reviews
    # Else the max specified number of reviews is used
    nReviewsToProecess = min(getNumberReviewsLoaded(driver), maxReviews) 
    
    print("All pages loaded. Attempting to scrap a total of {0} reviews".format(nReviewsToProecess))
    # Fetch every review
    for i in range(nReviewsToProecess):
        pos = i+1
        # Review rating
        rating = obtainSingleElementFromText(driver, getReviewFullXpath(pos, '//div[contains(@class, "ratings")]'), r'(\d+)/10')
        
        # Review title
        title = getReviewTextAtPos(driver, pos, '//a[@class="title"]')
        
        # Review username
        username = getReviewTextAtPos(driver, pos, '//span[@class="display-name-link"]')
        
        # Review date
        date_text = getReviewTextAtPos(driver, pos, '//span[@class="review-date"]')
        date = None
        if (date_text):
            date = datetime.strptime(date_text, '%d %B %Y').strftime("%d/%m/%Y")
            
        # Review helpful
        helpful = getReviewTextAtPos(driver, pos, '//div[contains(@class, "actions")]')
        match = re.search(r'^([\d\.]+) out of ([\d\.]+) found this helpful\.', helpful)
        helpfulYes = None
        helpfulTotal = None
        if (match):
            helpfulYes = match.group(1).replace(".","")
            helpfulTotal = match.group(2).replace(".","")

        # Review is spoiler
        isSpoiler = getReviewAtPos(driver, pos, '//span[(@class="spoiler-warning")]') != None
    
        # Review comment
        comment_element = getReviewAtPos(driver, pos, '//div[@class="content"]//div[contains(@class,"text show-more__control")]')
        comment = None
        if (comment_element):
            comment = re.sub(r'\s+',' ', comment_element.get_attribute('innerHTML'))        
        
        reviews_ret = reviews_ret + [{
            'movieId': movieId,
            'username':username,
            'date':date,
            'review_title':title,
            'rating':rating,
            'text':comment,
            'helpfulYes':helpfulYes,
            'helpfulTotal':helpfulTotal,
            'isSpoiler': isSpoiler
        }]
        
        print("Scraped review number: {0} for titleId: {1}. Review title: {2}".format(pos, movieId, title))
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
    '''
    STUB function
    '''
    reviews = []
    for movieId in moviesIds:
        reviews = reviews + getReviewsStub(driver, movieId, reviewOptions)
    return reviews

def getMoviesReviews(driver, moviesIds, reviewOptions):
    '''
    Obtains the reviews that matches the options from a list of movies
    '''
    reviews = []
    for movieId in moviesIds:
        print("Starting to scrap reviews for titleId: {0}".format(movieId))
        reviews = reviews + getReviews(driver, movieId, reviewOptions)
        print("Ended scraping reviews for titleId: {0}".format(movieId))
    return reviews
    