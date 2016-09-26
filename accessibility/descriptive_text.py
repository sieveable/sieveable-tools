#!/usr/bin/python
import glob
import os
import sys
import logging
import json
from optparse import OptionParser
from lxml import etree
from xml.etree.ElementTree import QName
from lxml.etree import ParserError
from lxml.etree import XMLSyntaxError

log = logging.getLogger("count_descriptive_text")
log.setLevel(logging.DEBUG)
namespace = "http://schemas.android.com/apk/res/android"

def count_elements(filename, element_name):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(filename, parser)
    attribute_full_name = str(QName(namespace, 'android:contentDescription'))
    total = tree.xpath('count(//' + element_name + ')')
    with_count = tree.xpath('count(//' + element_name + 
        '[@android:contentDescription])',
        namespaces={'android': 'http://schemas.android.com/apk/res/android'})
    without_count = tree.xpath('count(//' + element_name +
            '[not(@android:contentDescription)])',
            namespaces={'android': 'http://schemas.android.com/apk/res/android'})
    return (total, with_count, without_count)

def count_descriptive_text(element_name, source_dir, target_dir):
    count = 0
    result = []
    for f in glob.iglob(os.path.join(source_dir, '**/', '*.xml'), recursive=True):
        log.info("%i - Checking the number of " + element_name + " in %s",
                count, os.path.abspath(f))
        count +=1
        base_name = os.path.basename(f)
        base_name = os.path.splitext(base_name)[0]
        package_name = base_name.rsplit('-', 1)[0]
        version_code = base_name.rsplit('-', 1)[1]
        d = {"id": package_name + "-" + version_code,
                "packageName" : package_name, "versionCode": version_code,
                "total_" + element_name: 0, "count_with_contentDescription": 0,
                "count_without_contentDescription": 0}
        try:
            total, with_count, without_count = count_elements(f, element_name)
            d["total_"+element_name] = total
            d["count_with_contentDescription"] = with_count
            d["count_without_contentDescription"] = without_count
            result.append(d)
        except (ParserError, XMLSyntaxError) as e:
            log.error("Error in parsing file: %s", f)
            continue
    out_file = os.path.join(target_dir, element_name + '_descriptive_text_count.json')
    with open(out_file, 'w+') as fw:
        json.dump(result, fw, indent=0)
    log.info("Saved the result at %s", out_file)

def main(args):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logging_console = logging.StreamHandler(sys.stdout)
    logging_console.setFormatter(formatter)
    logging_console.setLevel(logging.DEBUG)
    log.addHandler(logging_console)
    usage_info = ''' python %prog <View> <source_directory> <target_directory> [options]

    Parses ui-xml files and counts how many <View> elements are defined with
    the android:contentDescription attribute in each app.

    View elements can be any Android View such as, ImageButton, ImageView, CheckBox, etc.
    The tool will attempt to recursively find xml files in source_directory. 
    Each xml file is expected to be named in the following naming schemes packageName-versionCode.xml.
    The result is a JSON file with the name "View_descriptive_text_count.json"
    '''
    parser = OptionParser(usage=usage_info, version="%prog 1.0")
    parser.add_option("-l", "--log", dest="log_file",
            help="write logs to FILE.", metavar="FILE")
    (options, args) = parser.parse_args()
    if options.log_file:
        logging_file = logging.FileHandler(options.log_file, mode='a',
                encoding='utf-8', delay=False)
        logging_file.setLevel(logging_level)
        logging_file.setFormatter(formatter)
        log.addHandler(logging_file)
    if len(args) != 3:
        parser.error("incorrect number of arguments.")
    cmd_list = ['ImageButton', 'ImageView', 'CheckBox']
    if args[0] not in cmd_list:
        sys.exit(args[0] + ". Error: unknown command. Valid commands are: " + ", ".join(cmd_list))
    if not os.path.isdir(args[1]):
        sys.exit("Error: source directory " + args[1] + " does not exist.")
    if not os.path.isdir(args[2]):
        sys.exit("Error: target directory " + args[2] + " does not exist.")
    count_descriptive_text(args[0], args[1], args[2])

if __name__ == '__main__':
    if sys.version_info >= (3,5):
        main(sys.argv[1:])
    else:
        sys.exit("ERROR: This tool requires Python version 3.5 or higher")
