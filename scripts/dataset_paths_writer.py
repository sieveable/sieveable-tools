#!/bin/python
import os
from os import path
import sys
from optparse import OptionParser
import json

dataset = {"dataset": {"listing": [], "ui": [], "manifest": [], "code": [] }}

def generate_target(source_dir, targetType):
    for root, dirs, files in os.walk(source_dir):
        if len(dirs) == 0:
            entry = {"target": root}
            dataset["dataset"][targetType].append(entry)

def main(args):
    parser = OptionParser(usage="python %prog manifest_root_dir ui_xml_root_dir out_json_file", version="%prog 1.0")
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Invalid number of arguments.")
    if os.path.exists(args[2]):
        sys.exit(args[0] + " already exists")
    generate_target(args[0], "manifest")
    generate_target(args[1], "ui")
    with open(args[2], "w") as f:
        f.write(json.dumps(dataset, indent=4, separators=(',', ': ')))
    print "dataset config (for leveldb) has been written at " + args[2]

main(sys.argv[1:])
