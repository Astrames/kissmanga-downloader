# kissmanga-downloader

Python script to batch-download images from [Kissmanga](https://kissmanga.com) and optionally convert them to PDF.
Forked from [Astrames/kissmanga-downloader](https://github.com/Astrames/kissmanga-downloader) and improved upon.

## Dependecies

You need Python 3.6+. Then, install the dependencies:

```bash
$  pip install -r requirements.txt
$  # Ubuntu&co
$  apt install chromium-chromedriver
$  # Arch&co
$  yay -S chromedriver
```


## Usage

Here is the output of the `-h` flag:

```
usage: kissmanga-downloader [-h] -u URL -i INI -e END [--pdf] [--pdfseries]
                            [--pagezero] [--ow]

Batch-download chapters and series from Kissmanga

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Name of the series, no need to include the base kissmanga
                     URL, so for 'https://kissmanga.com/Manga/Dragon-Ball'
                     use'Dragon-Ball)
  -i INI, --ini INI  Initial chapter number
  -e END, --end END  Final chapter number
  --pdf              Generate a PDF file for each chapter
  --pdfseries        Generate a huge PDF file with all chapters
  --pagezero         Create title page for each chapter
  --ow               Overwrite existing PDF files
```


## Features

*  Download all images/pages of a chapter and tidily organise them into folders with sane names.
*  Optionally create PDF files for each chapter and a PDF for the entire series, for convenience.

## Future Features

* Archiving the chapters into individual `.zip`,`.cbr` or `.cbz` files, depending on the user.
* More websites.

