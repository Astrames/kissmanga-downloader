# kissmanga-downloader

Python script to batch-download images from [Kissmanga](https://kissmanga.com) and optionally convert them to PDF.
Forked from [Astrames/kissmanga-downloader](https://github.com/Astrames/kissmanga-downloader) and improved upon.

## Dependecies

You need Python 3.6+. Then, install the dependencies:

```bash
$  pip install -r requirements.txt
```

### Windows

Download chromedriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it somewhere in your path (probably the same folder where you cloned this repo would be best).

### Linux

Get chromedriver from your distro repository. For example:

```bash
$  # Ubuntu&co
$  apt install chromium-chromedriver
$  # Arch&co
$  yay -S chromedriver
```

### macOS

No idea, just get and install chromedriver by whatever means you can.


## Usage

Here is the output of the `kissmanga-download -h`:

```
usage: kissmanga-downloader [-h] [-o OUTPUT] -u URL -i INI -e END [--pdf]
                            [--pdfseries] [--chapter_page] [--delay DELAY]
                            [--ow]

Batch-download chapters and series from Kissmanga

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder path where the series folder will be
                        created. Defaults to the current path from which this
                        script is run
  -u URL, --url URL     Name of the series, no need to include the base
                        kissmanga URL, so for
                        'https://kissmanga.com/Manga/Dragon-Ball' use'Dragon-
                        Ball)
  -i INI, --ini INI     Initial chapter number to download, in [1..n]
  -e END, --end END     Final chapter number to download, included
  --pdf                 Generate a PDF file for each chapter
  --pdfseries           Generate a huge PDF file with all chapters
  --chapter_page        Create title page for each chapter
  --delay DELAY         Add a delay (in seconds) between page downloads to
                        avoid overloading the server
  --ow                  Overwrite existing PDF files
```

For instance, to get the first 100 chapters of Dragon Ball, generating only chapter PDFs and adding a title page to each chapter and putting the results in `/output/folder/path`:

```bash
$  kissmanga-downloader -u Dragon-Ball -o /output/folder/path -i 1 -e 100 --pdf --pagezero --ow
```

## Features

*  Download all images/pages of a chapter and tidily organise them into folders with sane names.
*  Optionally create PDF files for each chapter and a PDF for the entire series, for convenience.

## Future Features

* Archiving the chapters into individual `.zip`,`.cbr` or `.cbz` files, depending on the user.
* More websites.

