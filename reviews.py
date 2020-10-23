

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
    reviews = []
    # TODO Scrap the content of the website and return a list of dictionaries with the same structure as getReviewsStub
    
    
    # END
    return reviews

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
    