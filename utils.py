

def internal_find_element_by_xpath(driver, xpath):
    '''
    Finds an element given its xpath
    Doesn't throw exception if the element is not found. Instaed None is returned
    '''
    try:
        return driver.find_element_by_xpath(xpath)
    except Exception:
        return None
        
def internal_find_element_by_xpath_text(driver, xpath):
    '''
    Finds an element given its xpath. Returns the element text inside the html tags
    Doesn't throw exception if the element is not found. Instaed None is returned
    '''
    try:
        return driver.find_element_by_xpath(xpath).text
    except Exception:
        return None
        
def getMovieUrl(movieId):
    '''
    Formats the movie identification inside the url that retrives the main page of the movie
    '''
    return "https://www.imdb.com/title/{0}/".format(movieId)