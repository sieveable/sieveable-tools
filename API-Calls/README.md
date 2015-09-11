# API calls extractor

A python script that extracts invoked methods from the smali files and stores them in one text file. Sieveable uses this tool to index and search API calls.


## Usage

```
Usage: python api_calls_extractor.py unpacked_apk_dir target_dir [options]

This tool recursively searches for invoke- methods calls from smali files and
store them in one text file.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROCESSES, --processes=PROCESSES
                        the number of worker processes to use. Default is the
                        number of CPU cores.
  -l FILE, --log=FILE   write logs to FILE.
  -v, --verbose         Increase verbosity.
  -d DEPTH_VALUE, --depth=DEPTH_VALUE
                        The depth of the child directories to scan for
                        AndroidManifest.xml files. Default is: 1
```

## Example

```
python api_calls_extractor.py ~/android-apps/unpacked/ ~/android-apps/api-calls/
```