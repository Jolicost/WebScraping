from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getResultMoviePattern(title, year):
    '''
    Obtains the regex pattern that matches the movie title from the results table element.
    If movie year is specified it will exactly try to match the movie that matches both title and release year
    Otherwise it will only match the title
    e.g. Titanic (1997) would match with title=titanic and optionally year=1997
    '''
    print(title)
    regex = None
    if (year != None):
        regex = re.compile(r"^\s*{0}.*\({1}\).*$".format(title,year), flags = re.IGNORECASE)
    else:
        regex = re.compile(r"^\s*{0}.*\(\d+\).*$".format(title), flags = re.IGNORECASE)
    return regex

# DEPRECATED
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

# DEPRECATED
def searchTitlesIds(driver, movies):
    '''
    Obtains the title id's from imdb given a list of movies {title, year (optional))
    '''
    ids = []
    for movie in movies:
        movieId = searchTitleId(driver, movie)
        if (movieId):
            ids = ids + [movieId]
            print("Scraped movie: {0}. Year specified: {1}. The movie id from imdb is: {2}".format(movie['title'],movie['year'],movieId))
        else:
            print("Failed to retrieve movieId from movie name: {0}. Year specified: {1}".format(movie['title'],movie['year']))
    return ids
   
def searchTitleIdWithoutFind(driver, search_bar, movie):
    '''
    Obtains a movie from the search bar without accessing /find
    '''
    # Clear the bar and input the movie title
    search_bar.clear()
    search_bar.send_keys(movie['title'])

    # Wait until the bar is loaded with the movies
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//ul[contains(@class,'anim-enter-done')]")))
    nMovies = len(element.find_elements_by_xpath("//li//div[@class='sc-ifAKCX KERZh']"))
    title_id = None
    # Iterate through each element of the results list which is a movie (not a video)
    for i in range(nMovies):
        pos = i + 1
        # Obtain the movie title and year from the divs inside the item
        movieTitle = element.find_element_by_xpath("((//li//div[@class='sc-ifAKCX KERZh'])[position()={0}]//div)[position()=1]".format(pos)).text
        movieYear = element.find_element_by_xpath("((//li//div[@class='sc-ifAKCX KERZh'])[position()={0}]//div)[position()=2]".format(pos)).text
        
        # Check if the given title is contained inside the item movie title
        if movie['title'].strip().lower() in movieTitle.strip().lower():
            # If the year is specified, check if it matches
            if movie['year'] == None or (movie['year'] and  movieYear.strip() == str(movie['year'])):
                # The year matches or the year is not specified, retrieve the url from the a tag in order to extract the movie identification
                url = element.find_element_by_xpath("((//li//div[@class='sc-ifAKCX KERZh'])[position()={0}])/ancestor::a[1]".format(pos))
                url_match = re.search(r'^.*\/title\/(.+)\?.*$', url.get_attribute("href"))
                if (url_match):
                    # Return the title id and stop searching for it on the first coincidence
                    title_id = url_match.group(1)
                    break
    return title_id 
    
def searchTitlesIdsWithoutFind(driver, movies):
    '''
    Obtains the title id's from imdb given a list of movies {title, year (optional)) Without accessing /find
    '''
    driver.get("https://www.imdb.com")
    search_bar = driver.find_element_by_xpath("//input[@id='suggestion-search']")
    ids = []
    for movie in movies:
        movieId = searchTitleIdWithoutFind(driver, search_bar, movie)
        if (movieId):
            ids = ids + [movieId]
            print("Scraped movie: {0}. Year specified: {1}. The movie id from imdb is: {2}".format(movie['title'],movie['year'],movieId))
        else:
            print("Failed to retrieve movieId from movie name: {0}. Year specified: {1}".format(movie['title'],movie['year']))
    return ids