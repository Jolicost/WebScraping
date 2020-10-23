from selenium import webdriver
from movies import searchTitlesIds
from reviews import getMoviesReviewsStub
from reviews import getMoviesReviews
from movie import getMoviesInfo
from movie import getMoviesGenres
from datetime import datetime
import csv
import yaml
import os

def getConfig():
    '''
    Reads the config file
    '''
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config

# Default config from file
config = getConfig()

def loadSeleniumDriver():
    '''
    Loads the selenium driver. Current supported browsers are Firefox and Chrome
    '''
    browser = config['browser']
    if (browser == 'firefox'):
        return webdriver.Firefox()
    elif (browser == 'chrome'):
        return webdriver.Chrome()
    else:
        raise Exception('browser not specified. Specify browswer in config.yaml file')

def loadMovies():
    '''
    Reads the movies to scrap from the configuration. 
    '''
    movies = config['movies']
    if (movies == None):
        raise Exception('no movies specified. Specify movie titles in config.yaml file')
    return movies

def writeDictionary(folder, filename, dictionary):
    '''
    Writes a list of dictionaries to the specified filename in csv format
    '''
    if (len(dictionary) == 0):
        print("No elements to write")
        return
    
    with open(os.path.join(folder, filename),'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, dictionary[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(dictionary)
        
def getDebugMode():
    '''
    Returns the debug mode specified in the options
    '''
    if (config['debug']['status'] == 1):
        return config['debug']['mode']
    else:
        return None
        
def createOutputfolder():
    '''
    Creates the execution output folder based on the current date and time
    '''
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    folder = "dataset_{0}".format(dt_string)
    os.mkdir(folder)
    return folder

   
def scrapFullMovie():
    '''
    Scraps the full movie. That consists in:
    1. searches the movie ids from a basic description (title, year)
    2. Obtains the list of reviews from any valid movie found
    3. Obtains the genres from the movies
    4. Obtains the basic information about the movies
    5. Creates the output folder and stores the dataset inside
    '''
    movies = loadMovies()
    driver = loadSeleniumDriver()
    ids = searchTitlesIds(driver, movies)
    reviewOptions = config['reviews']
    
    reviews = getMoviesReviews(driver, ids, reviewOptions)
    genres = getMoviesGenres(driver, ids)
    movies = getMoviesInfo(driver, ids)
    
    folder = createOutputfolder()
    
    writeDictionary(folder, 'reviews.csv', reviews)
    writeDictionary(folder, 'movies.csv', movies)
    writeDictionary(folder, 'genres.csv', genres)
    
    driver.close()
    
def debug_scrapReview():
    '''
    Debug function for scraping the reviews of a movie
    '''
    # Gladiator
    ids = ['tt0172495']
    driver = loadSeleniumDriver()
    reviewOptions = config['reviews']
    reviews = getMoviesReviews(driver, ids, reviewOptions)
    folder = createOutputfolder()
    writeDictionary(folder, 'reviews.csv', reviews)
    driver.close()
    
def debug_scrapMovie():
    '''
    Debug function for scraping the basic information of a movie
    '''
    # Gladiator and Saving private Ryan
    ids = ['tt0172495','tt0120815']
    driver = loadSeleniumDriver()
    movies = getMoviesInfo(driver, ids)
    folder = createOutputfolder()
    writeDictionary(folder, 'movies.csv', movies)
    driver.close()
    
def debug_scrapGenres():
    '''
    Debug function for scraping the genres of a movie
    '''
    # Gladiator and Saving private Ryan
    ids = ['tt0172495','tt0120815']
    driver = loadSeleniumDriver()
    genres = getMoviesGenres(driver, ids)
    folder = createOutputfolder()
    writeDictionary(folder, 'genres.csv', genres)
    driver.close()
    
if __name__ == '__main__':
    debug_mode = getDebugMode()
    if (debug_mode == None):
        scrapFullMovie()
    elif (debug_mode == 'reviews'):
        debug_scrapReview()
    elif (debug_mode == 'movies'):
        debug_scrapMovie()
    elif (debug_mode == 'genres'):
        debug_scrapGenres()
    