from selenium import webdriver
from movies import searchTitlesIds
from reviews import getMoviesReviewsStub
from reviews import getMoviesReviews
from datetime import datetime
import csv
import yaml
import os

def getConfig():
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config

config = getConfig()

def loadSeleniumDriver():
    browser = config['browser']
    if (browser == 'firefox'):
        return webdriver.Firefox()
    elif (browser == 'chrome'):
        return webdriver.Chrome()
    else:
        raise Exception('browser not specified. Specify browswer in config.yaml file')

def loadMovies():
    movies = config['movies']
    if (movies == None):
        raise Exception('no movies specified. Specify movie titles in config.yaml file')
    return movies

def writeDictionary(folder, filename, dictionary):
    if (len(dictionary) == 0):
        print("No elements to write")
        return
    
    with open(os.path.join(folder, 'reviews.csv'),'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, dictionary[0].keys())
        writer.writeheader()
        writer.writerows(dictionary)
def getDebugMode():
    if (config['debug']['status'] == 1):
        return config['debug']['mode']
    else:
        return None
def createOutputfolder():
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    folder = "dataset_{0}".format(dt_string)
    os.mkdir(folder)
    return folder

def scrapReviews():
    movies = loadMovies()
    driver = loadSeleniumDriver()
    ids = searchTitlesIds(driver, movies)
    reviewOptions = config['reviews']
    reviews = getMoviesReviewsStub(driver, ids, reviewOptions)
    folder = createOutputfolder()
    writeDictionary(folder, 'reviews.csv', reviews)
    driver.close()
    
def debug_scrapReview():
    # Gladiator
    ids = ['tt0172495']
    driver = loadSeleniumDriver()
    reviewOptions = config['reviews']
    reviews = getMoviesReviews(driver, ids, reviewOptions)
    folder = createOutputfolder()
    writeDictionary(folder, 'reviews.csv', reviews)
    driver.close()
    
if __name__ == '__main__':
    debug_mode = getDebugMode()
    if (debug_mode == None):
        scrapReviews()
    elif (debug_mode == 'reviews'):
        debug_scrapReview()
    