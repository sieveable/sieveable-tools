# Listing details parser
Scrape and extract apps' listing details information from the Google Play Store

## Usage

```
Usage: python listing-parser.py [options] google_play_html_page_file | packageName-versionCode

Parse listing details web page and store the data in JSON format

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o DIR, --out-dir=DIR
                        write out file to a target directory. Default is
                        current directory
  -l FILE, --log=FILE   write logs to FILE.
  -v, --verbose         Increase verbosity.
```

## Disclaimer

This tool is developed and released here for academic purposes only, and we are not responsible for any damage that could be done with it.
Use it at your own risk.

## License
This tool is licensed under the MIT license.