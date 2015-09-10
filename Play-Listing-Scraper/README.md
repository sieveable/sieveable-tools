# Play Listing Scraper
Scrape and extract apps' listing details information from the Google Play Store.

[![Build Status](https://travis-ci.org/sikuli/sieveable-tools.svg?branch=master)](http://travis-ci.org/sikuli/sieveable-tools) [![PyPI](https://img.shields.io/pypi/v/playlistingscraper.svg)](https://github.com/sikuli/sieveable-tools/tree/master/Play-Listing-Scraper) [![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/sikuli/sieveable-tools)


## Installation

### Installing from PyPI
```
pip install playlistingscraper
```

### Installing from source
```
$ git clone https://github.com/sikuli/sieveable-tools.git
$ cd Play-Listing-Scraper
$ sudo python setup.py install
```

## Usage

```
$ playlistingscraper --help
playlistingscraper [options] packageName-versionCode | google_play_html_page_file

A tool for Scraping an app's listing details data from the Google Play Store
store and saving it in a file in JSON format.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o DIR, --out-dir=DIR
                        write out file to a target directory. Default is
                        current directory
  -l FILE, --log=FILE   write logs to FILE.
  -v, --verbose         Increase verbosity.
```

## Example
```
$ playlistingscraper com.evernote-4535
$ ls
com.evernote-4534.listing.json
$ cat com.evernote-4534.listing.json
{
    "n": "com.evernote",
    "verc": "4535",
    "t": "Evernote",
    "cadd": "305 Walnut Street\nRedwood City, CA 94063",
    "cat": "Productivity",
    "crat": "Everyone",
    "crt": "Evernote Corporation",
    "curl": "/store/apps/developer?id=Evernote+Corporation",
    "dct": 100000000,
    "desc": "Evernote is the modern workspace that syncs between all of your devices.",
    "dtp": "August 30, 2015",
    "dtxt": "100,000,000 - 500,000,000",
    "new": "Bug fixes and miscellaneous improvements",
    "os": "Varies with device",
    "pri": "Free",
    "purl": "https://www.google.com/url?q=http://evernote.com/privacy/&sa=D&usg=AFQjCNHTyefT6GQ6A6mnOKPeqKUA_qjesg",
    "rate": 4.6,
    "rct": 1305159,
    "sz": "Varies with device"
}

```

###Field names symbol table:
Sieveable uses the output of this tool as the listing details data and stores it in a MongoDB collection. 

MongoDB stores all field names in every document which consumes disk space; therefore, we should use shorter field names. 
The following table shows the short names used in the public collection in MongoDB and their meanings.

|short name |  meaning                  |
|-----------|---------------------------|
| n         | apk name                  |
| t         | app title                 |
| desc      | description               |
| url       | play store URL            |
| cat       | category                  |
| pri       | price                     |
| dtp       | date published            |
| verc      | version code              |
| os        | operating systems         |
| rct       | ratings count             |
| rate      | rating                    |
| crat      | content rating            |
| crt       | creator                   |
| curl      | creator URL               |
| cadd      | creator address           |
| sz        | install size              |
| sztxt     | install size text         |
| dct       | downloads count           |
| dtxt      | downloads count text      |
| purl      | privacy statement url     |
| new       | what's new in this version|



## Disclaimer

This tool is developed and released here for academic purposes only, and we are not responsible for any damage that could be done with it.
Use it at your own risk.

## License
This tool is licensed under the MIT license.