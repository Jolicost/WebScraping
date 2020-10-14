from selenium.webdriver.common.keys import Keys
import time
import re

def getResultMoviePattern(title, year):
    '''
    Obtains the regex pattern that matches the movie title from the results table element.
    If movie year is specified it will exactly try to match the movie that matches both title and release year
    Otherwise it will only match the title
    e.g. Titanic (1997) would match with title=titanic and optionally year=1997
    '''
    regex = None
    if (year != None):
        regex = re.compile(r"^\s*{0}.*\({1}\).*$".format(title,year), flags = re.IGNORECASE)
    else:
        regex = re.compile(r"^\s*{0}.*\(\d+\).*$".format(title), flags = re.IGNORECASE)
    return regex

def searchTitleId(driver, movie):
    '''
    Obtains the title id from the given movie object
    The movie object specifies the movie title. Optionally, it could also specify the relase year, for a more specific search
    The first result from the table that matches the criteria is returned
    If no result matches, None is returned
    '''
    # Search movies by title
    driver.get("https://www.imdb.com/find?s=tt&q={0}".format(movie['title']))
    # Find the td elements with result_text as class contained by a table with class="findList"
    table_results = driver.find_elements_by_xpath("//table[contains(@class, 'findList')]//td[contains(@class,'result_text')]")
    # Obtain the regex object that matches the text inside the previous td element
    regex = getResultMoviePattern(movie['title'], movie['year'])    
    title_id = None
    for result in table_results:
        if (regex.match(result.text)):
            # If the movie title matches the pattern, then the title id from imdb can be extracted from the hyperlink
            url = result.find_element_by_xpath("./a").get_attribute("href")
            url_match = re.search(r'^.+\/title\/(.+)\/.*$',url)
            if (url_match):
                title_id = url_match.group(1)
                break
    return title_id

def searchTitlesIds(driver, movies):
    '''
    Obtains the title id's from imdb given a list of movies {title, year (optional)
    '''
    ids = []
    for movie in movies:
        movieId = searchTitleId(driver, movie)
        ids = ids + [movieId]
        print("Scrapped movie: {0}. Year specified: {1}. The movie id from imdb is: {2}".format(movie['title'],movie['year'],movieId))
    return ids