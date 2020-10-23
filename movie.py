import re
from utils import internal_find_element_by_xpath
from utils import internal_find_element_by_xpath_text
from utils import getMovieUrl

def obtainSingleElementFromText(driver, xpath, regex):
    '''
    Retrives the element text and applies a regex pattern with only 1 group
    If the element is not found or the patter does not match None is returned
    '''
    element = internal_find_element_by_xpath(driver, xpath)
    if (element):
        matches = re.search(regex, element.text)
        if (matches):
            return matches.group(1)
    
    return None

def obtainMoneyAmountFromElementText(driver, xpath):
    '''
    Retrives an element given its xpath and parses the amount as money_regex
    e.g. $100,300,143.3 would be parsed as 100300143.3 
    '''
    money_regex = r'^.*\$([\d\,\.]+).*$'
    money_text = obtainSingleElementFromText(driver, xpath, money_regex)
    if (money_text):
        return float(money_text.replace(",",""))
    return None
        
def getMovieInfo(driver, movieId):
    '''
    Obtains the basic data of a movie given its id
    All the information is contained in the same page
    The output consists of a dictionary with the movie properties
    If any property is not found or not correctly formatted it will be set to None
    '''
    driver.get(getMovieUrl(movieId))
    # Movie original title
    movie_title = obtainSingleElementFromText(driver, "//div[@id='title-overview-widget']//div[@class='originalTitle']",r'^\s*(.*?)\s*\(original title\)$')
     
    # Movie year and title if original title was not found
    title_text = internal_find_element_by_xpath_text(driver, "//div[@id='title-overview-widget']//div[@class='title_wrapper']//h1")
    if (title_text):
        matches = re.search(r'^\s*(.*?)\s*\((\d+)\)$', title_text)
        movie_year = None
        if (matches):
            movie_title = movie_title if movie_title else matches.group(1)
            movie_year = matches.group(2)
        
    # Movie duration
    minutes = obtainSingleElementFromText(driver,"//div[@id='titleDetails']//h4[normalize-space(text()) = 'Runtime:']/..//time",r'^(\d+)\s+min$')
    
    # Rating and number of votes
    rating_text = internal_find_element_by_xpath_text(driver, "//div[contains(@class, 'imdbRating')]//span[@itemprop='ratingValue']")
    rating = float(rating_text.replace(",",".")) if rating_text else None
    
    nVotes_text = internal_find_element_by_xpath_text(driver, "//div[contains(@class, 'imdbRating')]//span[@itemprop='ratingCount']")
    nVotes = int(nVotes_text.replace(".","")) if nVotes_text else None
    
    # Popularity
    popularity = obtainSingleElementFromText(driver,"//div[contains(@class,'titleReviewBar')]//div[normalize-space(text()) = 'Popularity']/..//span[@class='subText']", r'^(\d+)\s+.*$')
    
    # Budget and gross
    budget = obtainMoneyAmountFromElementText(driver, "//div[@id='titleDetails']//h4[normalize-space(text()) = 'Budget:']/..")
    gross = obtainMoneyAmountFromElementText(driver, "//div[@id='titleDetails']//h4[normalize-space(text()) = 'Cumulative Worldwide Gross:']/..")
    
    # Final structure
    return {
        'movieId': movieId,
        'movieTitle':movie_title,
        'movieYear':movie_year,
        'duration': minutes,
        'rating':rating,
        'nVotes':nVotes,
        'popularity':popularity,
        'budgetUSD':budget,
        'grossUSD':gross
    }
  
def getMovieGenres(driver, movieId):
    '''
    Scraps the genres of a movie given its id
    The output consists of a list of dictionaries. Each of those contains the movieId and the genre text
    '''
    driver.get(getMovieUrl(movieId))
    genres_text = internal_find_element_by_xpath_text(driver, "//div[@id='titleStoryLine']//h4[normalize-space(text()) = 'Genres:']/..")
    if (genres_text):
        matches = re.search(r'^Genres:\s*(.+)\s*$', genres_text)
        if (matches):
            genres = [genre.strip() for genre in matches.group(1).split("|")]
            return [{'movieId':movieId,'genre':genre} for genre in genres]
    return []
    
def getMoviesGenres(driver, moviesIds):
    '''
    Scraps the genres of a set of movies
    '''
    genres = []
    for movieId in moviesIds:
        movie_genres = getMovieGenres(driver, movieId)
        genres = genres + movie_genres
        if (len(movie_genres) > 0):
            print("Scraped genres for titleId: {0}".format(movieId))
        else:
            print("No genres found for titleId: {0}".format(movieId))
    return genres

def getMoviesInfo(driver, moviesIds):
    '''
    Scraps the basic information of a set of movies
    '''
    movies = []
    for movieId in moviesIds:
        movies = movies + [getMovieInfo(driver, movieId)]
        print("Scraped movie information for titleId: {0}".format(movieId))
    return movies
    