#!/usr/bin/env python

import os
import time
import sys
import re
import inspect
import pdfMaker
import argparse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


"""
sample url =
http://kissmanga.com/Manga/Sensei-Lock-On
http://kissmanga.com/Manga/Dragon-Ball
"""


class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg


class DriverX(object):
    """docstring for  driverX"""
    def __init__(self):
        super(DriverX, self).__init__()
        self.driver = init_driver()

    def __enter__(self):
        return self.driver

    def __exit__(self, type, value, traceback):
        pass


def init_driver():
    """
    Returns a driver object.
    """

    # Setting the user agent to a human browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53")

    chrome_init = inspect.getfullargspec(webdriver.Chrome)

    if 'options' in chrome_init.args:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(chrome_options=options)

    driver.set_page_load_timeout(90)
    return driver


def gather_xml_info(driver, title_text):
    """
    Dig through the first page and gather data for a Comicinfo.xml file
    """
    xml_root = ET.Element('ComicInfo',
                          {'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                           'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'})

    xml_series = ET.SubElement(xml_root, 'Series')
    xml_series.text = title_text
    try:
        author = driver.find_element_by_xpath("//div[contains(@class, 'author-content')]/a")
        xml_author = ET.SubElement(xml_root, 'Writer')
        xml_author.text = author.get_attribute('innerHTML')
    except NoSuchElementException:
        pass

    try:
        artist = driver.find_element_by_xpath("//div[contains(@class, 'artist-content')]/a")
        xml_artist = ET.SubElement(xml_root, 'Penciller')
        xml_artist.text = artist.get_attribute('innerHTML')
    except NoSuchElementException:
        pass

    try:
        genre = driver.find_elements_by_xpath("//div[contains(@class, 'genres-content')]/a")
        genre_str = ""
        for elem in genre:
            genre_str = genre_str + ',' + elem.get_attribute('innerHTML')
        genre_str = genre_str[1:]
        xml_genre = ET.SubElement(xml_root, 'Genre')
        xml_genre.text = genre_str
    except NoSuchElementException:
        pass

    try:
        summary = driver.find_elements_by_xpath("//div[contains(@class, 'summary__content')]/p")
        summary_str = ""
        for elem in summary:
            summary_str = summary_str + '\n' + elem.get_attribute('innerHTML')
        summary_str = summary_str[1:]
        xml_summary = ET.SubElement(xml_root, 'Summary')
        xml_summary.text = summary_str
    except NoSuchElementException:
        pass

    return xml_root


def get_title_and_chapter_links(driver, url_to_series, reverse=False):
    """
    Supply the main page of the manga and get the title, and list of URLs
    of the chapters available
    """
    driver.get(url_to_series)

    try:
        title_tag = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,"post-title")))
        title_text = title_tag.text.encode("ascii", errors="ignore").decode()
    except TimeoutException:
        print("Exception Occured:    TimeoutException")
        sys.exit("Couldn't get title!")

    if '\n' in title_text:
        title_text = title_text[(title_text.index('\n') + 1):]

    xml_root = gather_xml_info(driver, title_text)

    list_of_a_tags = driver.find_elements_by_xpath("//li[contains(@class, 'wp-manga-chapter ')]/a")

    # Reversing to get ascending list,
    # since it is originally in descending order
    if not reverse:
        list_of_a_tags = list_of_a_tags[::-1]

    list_of_href = []
    for a_tag in list_of_a_tags:
        list_of_href.append(a_tag.get_attribute('href'))

    return title_text, list_of_href, xml_root


def download_pages_of_one_chapter(driver, url_to_chapter, xmlroot,
                                  series_folder, delay=0):
    """
    Goes through the chapter and downloads each page it encounters
    Returns -1 if error, 0 if normal, 1 if already exists.
    """

    # Find out chapter name
    chapter_name = (url_to_chapter.rsplit('/')[-2])
    if chapter_name.endswith('.'):
        chapter_name = chapter_name[:-1]

    # Unify format by parsing number out of chapter_name
    chapter_number = (re.findall(r'\d+.?\d*', chapter_name)[0]).replace('-', '.')
    chapter_folder_name = "Chapter-" + chapter_number
    if chapter_folder_name.endswith('.'):
        chapter_folder_name = chapter_folder_name[:-1]

    if os.path.exists(chapter_folder_name + '.pdf') or os.path.exists(chapter_folder_name + '.cbz'):
        print("Skipping " + chapter_folder_name + " due to cbz/pdf.")
        return 1

    # Going to first page
    try:
        driver.get(url_to_chapter)
    except TimeoutException:
        print("Couldn't load chapter: " + url_to_chapter)
        return -1

    os.chdir(series_folder)

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "reading-style-select")))
    except TimeoutException:
        print("Exception Occured:    TimeoutException")
        print("Couldn't load chapter: " + url_to_chapter)
        return -1

    list_of_page_img = driver.find_elements_by_xpath('//img[@class="wp-manga-chapter-img"]')

    # Get all chapter image locations
    img_urls = []
    for page_img in list_of_page_img:
        img_urls.append(page_img.get_attribute("src"))

    # Create folder for chapter , if it not exist
    if not os.path.exists(chapter_folder_name):
        os.makedirs(chapter_folder_name)

    print("Chapter " + chapter_name + " -> " + chapter_folder_name + os.path.sep)

    xml_title = ET.SubElement(xmlroot, 'Title')
    xml_title.text = 'Chapter ' + chapter_number
    xml_number = ET.SubElement(xmlroot, 'Number')
    xml_number.text = chapter_number
    xml_fp = os.path.join(chapter_folder_name + os.path.sep + 'ComicInfo.xml')
    tree = ET.ElementTree(xmlroot)
    with open(xml_fp, 'wb') as xml_file:
        tree.write(xml_file)

    page_num = 1
    good_downloads = actual_downloads = 0
    for img_url in img_urls:

        page_num_pad = str(page_num).zfill(3)
        filepath = os.path.join(chapter_folder_name, page_num_pad + ".jpg")

        # Creating full file name
        fullfilename = os.path.join(series_folder, filepath)

        if os.path.exists(fullfilename):
            print(" " + page_num_pad + "(exists)", end="")
            good_downloads = good_downloads + 1
        else:
            print(" " + page_num_pad, end="")
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': "Magic Browser"})
                con = urllib.request.urlopen(req)
                img_good = True
                img_data = con.read()
                try:
                    img_data.decode('utf-8')
                    img_good = False
                except UnicodeError:
                    pass
                if img_good:
                    with open(fullfilename, mode="wb") as d:
                        d.write(img_data)
                        good_downloads = good_downloads + 1
                        actual_downloads = actual_downloads + 1
                else:
                    raise Exception('Not an Image')
                if delay > 0:
                    time.sleep(delay)
            except Exception as e:
                # Skip, not available
                print("(ERROR)", end="")
                print(e, end=" ")

        sys.stdout.flush()
        page_num += 1

    if good_downloads == 0:
        os.remove(xml_fp)
        os.rmdir(chapter_folder_name)
        print()
        print('Unable to download any images')
        return -1

    print()
    print()

    if actual_downloads == 0:
        return 1

    return 0


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


def make_filename(dirname, ext):
    if dirname.endswith("/"):
        dirname = dirname[:-1]
    return "%s.%s" % (dirname, ext)


def create_cbz_pdf(args, series_folder):
    if args.cbz:
        for root, dirs, files in os.walk(series_folder):
            dirs.sort()
            for single_dir in dirs:
                cbz_filename = make_filename(single_dir, 'cbz')
                with zipfile.ZipFile(cbz_filename, "w") as zfile:
                    print("Creating: " + cbz_filename)

                    for rootpath, dirnames, filenames in os.walk(single_dir):
                        for filename in filenames:
                            abs_filename = os.path.join(rootpath, filename)
                            if filename == 'ComicInfo.xml':
                                zfile.write(abs_filename, arcname=filename)
                            else:
                                zfile.write(abs_filename)
                            if args.delete_jpg:
                                os.remove(abs_filename)
                    zfile.close()
                    if args.delete_jpg:
                        os.rmdir(single_dir)

    if args.pdf:
        # Active directory is inside the series folder:
        # Create the PDF, from the chapters inside
        for root, dirs, files in os.walk(series_folder):
            dirs.sort()
            for single_dir in dirs:
                pdfMaker.create_pdf(imageDirectory=single_dir,
                                    bool_page0=args.chapter_page,
                                    overwriteExisting=args.overwrite)

    if args.pdf_series:
        pdfMaker.merge_pdfs(series_folder)


def process_one_url(driver, url, output_folder, args):
    """
    Fully process one URL, return number of chapters downloaded.
    """

    # Fetch list of URLs
    nrof_urls = 0
    tries = 5
    print("Getting server URLs", end="")
    sys.stdout.flush()
    while nrof_urls == 0 and tries > 0:
        title, list_of_hrefs, xmlroot = get_title_and_chapter_links(driver, url, args.reverse)
        nrof_urls = len(list_of_hrefs)
        tries = tries - 1
        print(".", end="")
        sys.stdout.flush()
        time.sleep(2)

    print(" Done! (%d URLs)" % len(list_of_hrefs))
    if nrof_urls == 0:
        print("Can't connect, or no chapters found")
        return 0

    # Series folder
    series_folder = os.path.join(output_folder, title)

    print("Preparing output folder: %s" % series_folder)
    # Create folder for the series, if it doesn't exist
    if not os.path.exists(series_folder):
        os.makedirs(series_folder)

    # Navigate inside the series folder
    os.chdir(series_folder)

    if args.reverse:
        required_list = list_of_hrefs
    else:
        low_index = args.ini
        high_index = args.end

        if low_index < 1:
            print("--ini must be larger than 0: " + low_index)
            exit(0)

        if high_index < low_index and high_index != -1:
            print("--end must be greater or equal than --ini: [%d <= %d]" % (low_index, high_index))
            exit(0)

        if high_index == -1:
            required_list = list_of_hrefs[low_index - 1:]
        else:
            required_list = list_of_hrefs[low_index - 1: high_index]

    nrofchap = len(required_list)
    goodchap = 0

    if args.reverse:
        print("Starting chapter download in reverse order")
        print()
    else:
        print("Starting chapter download: %d to %d\n" % (low_index, high_index))

    # Iterate over the list_of_hrefs for the requested chapters
    for href in required_list:
        # Download a chapter
        ret = download_pages_of_one_chapter(driver, href, xmlroot,
                                            series_folder, args.delay)
        if ret == 0:
            goodchap = goodchap + 1
        if args.reverse and ret == 1:
            # we hit a manga we have already.
            break

    print("%d of %d chapters downloaded successfully" % (goodchap, nrofchap))

    if args.cbz or args.pdf:
        print("Starting creation of PDF/CBZ files")
        create_cbz_pdf(args, series_folder)

    return goodchap


def process(driver):
    base_url = "https://kissmanga.in/kissmanga/"

    # Parse arguments
    parser = argparse.ArgumentParser(description="Batch-download chapters and series from Kissmanga")
    parser.add_argument('-o', '--output', type=str,
                        help="Output folder path where the series folder will be created. Defaults to the current path from which this script is run")
    parser.add_argument('-u', '--url', required=True, type=str,
                        help="Name of the series, no need to include the base kissmanga URL, so for 'https://kissmanga.in/kissmanga/dungeon-meshi' use 'dungeon-meshi')")

    parser_group = parser.add_mutually_exclusive_group(required=False)
    parser_group.add_argument('-i', '--ini', type=int, default=1,
                              help="Initial chapter number to download, in [1..n]")
    parser_group.add_argument('-r', '--reverse', action='store_true',
                              default=False,
                              help="Download in reverse order, stop when existing downloads are found.")

    parser.add_argument('-e', '--end', required=False, type=int, default=-1,
                        help="Final chapter number to download, included")
    parser.add_argument('--pdf', required=False, action='store_true',
                        help="Generate a PDF file for each chapter")
    parser.add_argument('--cbz', required=False, action='store_true',
                        help="Generate a CBZ file for each chapter")
    parser.add_argument('--delete_jpg', required=False, action='store_true',
                        help="Delete jpg files after cbz creation")
    parser.add_argument('--pdf_series', required=False, action='store_true',
                        help="Generate a huge PDF file with all chapters")
    parser.add_argument('--chapter_page', required=False, action='store_true',
                        help="Render a chapter page and put it in front of the PDF of each chapter")
    parser.add_argument('--delay', required=False, type=float, default=0.0,
                        help="Add a delay (in seconds) between page downloads to avoid overloading the server")
    parser.add_argument('--ow', required=False, action='store_true',
                        help="Overwrite existing PDF files")

    args = parser.parse_args()

    print("Initialising kissmanga-downloader")

    # Get main page of the series
    url = args.url if 'kissmanga.in' in dequote(args.url) else base_url + dequote(args.url)

    # Output folder
    output_folder = os.getcwd() if args.output is None else args.output
    try:
        os.chdir(output_folder)
    except Exception as e:
        print("Unable to change directory to " + output_folder)
        print(e)
        sys.exit(1)

    # Delay between page downloads
    if args.delay > 0:
        print("Using a delay of %.1f seconds" % args.delay)

    process_one_url(driver, url, output_folder, args)
    os.chdir(output_folder)

    driver.quit()
    print("Done!")


if __name__ == '__main__':
    with DriverX() as driver:
        process(driver)
