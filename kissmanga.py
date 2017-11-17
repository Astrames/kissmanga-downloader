# kissmanga

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import urllib.request 
import os

import make_pdf

"""
sample url = 
http://kissmanga.com/Manga/Sensei-Lock-On
http://kissmanga.com/Manga/Dragon-Ball
"""
def init_driver():
    """
    Returns a driver object.
    """

    driver = webdriver.Chrome()
    
    # driver.wait = WebDriverWait(driver, 5)
    return driver


def get_title_and_chapter_links(driver, url_to_series):
    """
    Supply the main page of the manga and get the title, and list of URLs
    of the chapters available
    """
    driver.get(url_to_series)

    title_tag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"bigChar")))
    title_text = title_tag.text
    
    # Debug statement
    # print(title_text)

    # tbody = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME,"tbody")))
    
    list_of_a_tags = driver.find_elements_by_xpath("//tbody/tr/td/a")

    # Reversing since it is originally in descending order
    list_of_a_tags = list_of_a_tags[::-1]

    list_of_href = []
    for a_tag in list_of_a_tags:
        # print("{0}  == {1}".format(a_tag.text,a_tag.get_attribute('href')))
        list_of_href.append(a_tag.get_attribute('href'))

    return title_text, list_of_href


def download_pages_of_one_chapter(driver, url_to_chapter):
    """
    Goes through the chapter and downloads each page it encounters
    """

    # Going to first page
    driver.get(url_to_chapter)

    ''' 
    # Process to get image src for each page
    image_tag = driver.find_element_by_xpath('//div[@id="divImage"]/img')
    print(image_tag.get_attribute('src'))
    '''

    # Doesn't work when using from Python shell
    # select = Select(driver.find_element_by_id("selectReadType"))

    # Alternative try
    drop_down_list = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,"selectReadType")))
    select = Select(drop_down_list)

    select.select_by_value('1')

    list_of_page_img = driver.find_elements_by_xpath('//div[@id="divImage"]/p/img')

    chapter_name = url_to_chapter[url_to_chapter.rfind('/') + 1 : url_to_chapter.rfind('?')]
    # chapter_name = chapter_name[:chapter_name.find('?') + 1]

    # Debug statement
    print("Chapter name is " + chapter_name)

    # Create folder for chapter , if it not exist
    if not os.path.exists(chapter_name):
        print("Chapter "+ chapter_name +" folder didnt exist, it has been created")
        os.makedirs(chapter_name)



    print("Downloading Chapter "+ chapter_name)
    



    page_no = 1
    for page in list_of_page_img:
        
        # Debug statement
        # print(page.get_attribute("src"))
        
        page_no_correct = str(page_no).zfill(3)

        url = page.get_attribute("src")
        filepath = chapter_name + "\\" + page_no_correct+".jpg"

        # Current folder
        pwd = os.path.dirname(os.path.realpath(__file__))

        

        #Creating full file name
        fullfilename = os.path.join(pwd, filepath)
        
        if os.path.exists(fullfilename):
            print("File " + page_no_correct + " exists! Skipping file...")
        else:
            print("Downloading Page " + page_no_correct + " ...")
            urllib.request.urlretrieve(url, fullfilename)
        

        page_no += 1


    pass
    

def create_series_folder(title):
     if not os.path.exists(title):
        print(title +" folder didnt exist, it has been created")
        os.makedirs(title)


def main1():
    """
    # Basic working of app
    url = input("Input url to kissmanga page: ")

    driver = init_driver()
    title, list_of_hrefs = get_title_and_chapter_links(driver, url)

    """


    # For downloading one chapter
    # download_pages_of_one_chapter(driver, list_of_hrefs[0])

    # To get indexes of the chapters to be downloaded:
    """
    low_chapter = input("Enter lower chapter url:")
    high_chapter = input("Enter higher chapter url:")

    low_index = -1
    high_index = -1

    for index, chapter in enumerate(list_of_hrefs):
        if low_index == -1 and low_chapter in chapter:
            low_index = index
        if high_index == -1 and high_chapter in chapter:
            high_index = index

    

    print(low_index, high_index)

    """

    print(os.getcwd())
    # Navigates to directory
    os.chdir("Akatsuki!! Otokojuku")

    print(os.getcwd())
    


    # driver.quit()



if __name__ == '__main__':

    # Basic working of app
    
    # Get main page of the series
    url = input("Input url to kissmanga page: ")

    driver = init_driver()
    title, list_of_hrefs = get_title_and_chapter_links(driver, url)

    
    
    # Create folder for the series, if it doesn't exist
    create_series_folder(title)

    # Starting folder
    start_folder = os.getcwd()

    # Navigate inside the series folder
    os.chdir(title)

    # Get indexes of the chapters to be downloaded
    low_chapter = input("Enter lower chapter url:")
    high_chapter = input("Enter higher chapter url:")

    low_index = -1
    high_index = -1

    for index, chapter in enumerate(list_of_hrefs):
        if low_index == -1 and low_chapter in chapter:
            low_index = index
        if high_index == -1 and high_chapter in chapter:
            high_index = index


    required_list = list_of_hrefs[low_index: high_index + 1]


    # Iterate over the list_of_hrefs for the requested chapters
    for href in required_list:

        # Download a chapter
        download_pages_of_one_chapter(driver, href)


    print("Chapters have been downloaded.")
    print("Make any required renames for the chapter folders, if you wish.")
    print("DO NOT RENAME THE SERIES FOLDER")
    input("Press enter to continue.")


    # Active directory is inside the series folder:
    # Create the PDF, from the chapters inside
    mypath = os.getcwd()
    for root, dirs, files in os.walk(mypath):
        for single_dir in dirs:
            make_pdf.pdf_from_images(single_dir)


    # Current folder has all the .pdf of the chapter folders
    make_pdf.merge_pdfs(os.getcwd())

    # Go back to start_folder
    os.chdir(start_folder)
    driver.quit()


    input("Press enter to exit")