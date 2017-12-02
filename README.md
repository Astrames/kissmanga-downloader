# kissmanga-downloader
Python script which will help downloading manga from kissmanga.com

# Introduction
Kissmanga Downloader is a command line tool to download manga from http://kissmanga.com/

  - Don't forget to read the ["Settings.ini"]  



## Table Of Content
* [Dependencies Installation](https://github.com/Astrames/kissmanga-downloader#dependencies-installation)
* [Installation](https://github.com/Astrames/kissmanga-downloader#installation)
* [Settings.ini File](https://github.com/Astrames/kissmanga-downloader#settingsini-file)
* [Usage](https://github.com/Xonshiz/ReadComicOnline-Downloader#usage)
* [Features](https://github.com/Astrames/kissmanga-downloader#features)
* [Future Features](https://github.com/Astrames/kissmanga-downloader#future-features)


## Dependecy Installation

* Install Python 3.6 from [here](https://www.python.org/downloads/release/python-363/)

* Add it to the system PATH (if not already added.)
	
    For Windows, refer https://superuser.com/questions/143119/how-to-add-python-to-the-windows-path)

* Install the dependencies by copying [this file](requirements.txt) to a folder, then go to that folder in the command prompt and then run,

	`pip install -r requirements.txt`


## Installation

If you haven't come across an error so far, you are good to go!

You need to clone or download the repository, and extract it where you want to store your downloaded manga.

For example,

If you want to store your manga in C:\Downloads\

Then

Extract the repository in the Downloads folder as

	C:\Downloads\kissmanga-downloader\
    
Downloaded manga will be stored inside this folder.

## Settings.ini file

Inside this file, you can choose appropriate parameters for downloading manga.

`Issue PDF` decides if you want to create a `.pdf` file of each chapter, after you're done downloading them.

`Series PDF` decides if you want to create a single `.pdf`, made from combining all the `Issue PDF` for that series.

`Page Zero` represents if you want to create a title page, which has the name of the chapter written on it. This is useful when you are reading a `Series PDF` and you wish to know which chapter you are currently reading.




## Usage

You just need to execute the `kissmanga.py` file to run the downloader.

We will see how to download Chapters 221-230 of [Dragon Ball](http://kissmanga.com/Manga/Dragon-Ball).

* Open your command prompt/Terminal and browse to this directory that has this script.

* Type `python kissmanga.py` to execute the script.

* Press Enter/Return.

* The script will now show the settings, obtained from the `settings.ini` file.

* Enter the URL for the main manga page, ie "http://kissmanga.com/Manga/Dragon-Ball"

* Wait for a second, as the script acquires data about the manga and creates a folder for it.

* The script will now prompt you, for the first and last URLs for the set of chapters you want to download.
	Let's say, you want to download chapter 221 to 230. Then you will enter

	`Enter lower chapter url:http://kissmanga.com/Manga/Dragon-Ball/Chapter-221?id=260807`
	
    `Enter higher chapter 	url:http://kissmanga.com/Manga/Dragon-Ball/Chapter-230?id=260816`

  
* Now, sit back and wait for the script to download all the chapters.

* After it's done downloading the chapters, it will prompt you, asking if you wish to rename any chapter folders.
	
    **Note**: I put in this prompt since chapters can often be named as "Chapter 67", "Chapter 67.5". We now that 67 should be the first in the reading order, but Windows atleast, sorts the folders so that 67.5 comes before 67. Hence, in the `Series PDF`, you may get the chapters in the wrong order. 
    
    To prevent that from happening, I suggest that you keep track of such chapters with decimal points in their names (like 67.5) and then rename the "67" to "67.0" to preserve the reading order.
    	
* Press Enter/Return to continue.        

* If you had selected the PDF options, then the `.pdf(s)` will now be created.


## Features

* Downloads all images/pages of a chapter and puts them in the chapter's respective folder.

* All chapter folders, are created inside a Series folder.

* You can read the manga in a `.pdf` directly, without having to create the `.pdf`. yourself


## Future Features

* Archiving the chapters into individual `.zip`,`.cbr` or `.cbz` files, depending on the user.

* More websites.


