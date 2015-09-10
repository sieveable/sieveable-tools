# Copy Manifest Files

A python script that searches for AndroidManifest.xml files in a given directory and copies them into a target directory after renaming them as packageName-versionCode.


## Usage
```
$ python copy_manifest.py -h
Usage: copy_manifest.py [options] search_directory target_manifest_files_dir

copy_manifest.py -- Recursively search for AndroidManifest.xml files in
search_directory and copy them to target_manifest_files_dir

Options:
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  -l FILE, --log=FILE  write logs to FILE.
```

## Example
```
$ ls ~/android-apps/unpacked/
└── com.eclipsim.gpsstatus2-83
    ├── AndroidManifest.xml
    ├── apktool.yml
    ├── res
    ├── smali
    ├── assets
└── com.alphonso.pulse-112
    ├── AndroidManifest.xml
    ├── apktool.yml
    ├── res
    ├── smali
    ├── assets

$ python copy_manifest.py ~/android-apps/unpacked/ ~/android-apps/manifest-files/

$ ls ~/android-apps/manifest-files/
com.alphonso.pulse-112.xml     com.eclipsim.gpsstatus2-83.xml
```

## LICENSE
MIT