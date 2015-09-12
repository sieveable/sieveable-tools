# Apktool Executor
A python script that runs [apktool](https://ibotpeaches.github.io/Apktool/) 
on a list of APK files. The goal of this tool is to simplify decompiling a large list of APK files.

It takes a list of APK files (text file that contains a list of apk path names or comma separated APK path names) as input and spawns a number of worker processes where each process runs apktool on each apk file, saves the unpacked apk file as packageName-versionCode,
and stores the decoded APKs under a single parent directory.

## Requirements

You must download the following tools and edit the config file (`apktool_executor.config`) with their full path names:

- [apktool](https://ibotpeaches.github.io/Apktool) version 2.0 or higher.
- Android _aapt_. This is required to obtain the package name and version code of the APK file and use that as the name of the decoded APK directory. To download aapt, download the [Android SDK Tools](http://developer.android.com/sdk/index.html), and you can find aapt under `sdk/build-tools/VERSION_NUMBER/aapt`.


## Usage:
```
$ python apktool_executor.py -h
Usage: python apktool_executor.py <apk_path_file | comma_separated_apk_path_names> target_directory [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROCESSES, --processes=PROCESSES
                        the number of worker processes to use. Default is the
                        number of CPUs in the system.
  -w FRAMEWORK_DIR, --framework=FRAMEWORK_DIR
                        forces apktool to use framework files located in
                        <FRAMEWORK_DIR>.
  -t TAG, --tag=TAG     forces apktool to use framework files tagged by <TAG>.
  -s, --no-src          Do not decode sources.
  -r, --no-res          Do not decode resources.
  -l FILE, --log=FILE   write logs to FILE.
  -v, --verbose         increase verbosity.
```

## Example:
``` 
$ cat ~/apk-files.txt 
/Users/droid/android-apps/apks/com.alphonso.pulse-112.apk
/Users/droid/android-apps/apks/com.eclipsim.gpsstatus2-83.apk

$ python apktool_executor.py ~/apk-files.txt ~/android-apps/unpacked/ -l ~/apktool.log
```

## LICENSE
MIT