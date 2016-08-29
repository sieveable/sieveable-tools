#!/bin/python
import os
from os import path
import sys
from optparse import OptionParser

def extract(inputdir, targetdir):
    targetpath = path.abspath(targetdir)
    inputpath = path.abspath(inputdir)
    for f in os.listdir(inputpath):
        if f.endswith(".tar.bz2"):
            filepath = path.join(inputpath, f)
            basename = path.basename(filepath).split(".")[0]
            partname = basename[basename.rfind("-") + 1 : len(basename)]
            target = path.join(targetpath, partname)
            print "mkdir " + target
            os.mkdir(target)
            cmd = "tar -xjf " + filepath + " -C " + target + " --strip-components=1"
            print cmd
            rcode = os.system(cmd)
            if rcode != 0:
                print "Failed to extract " + filepath
            else:
                print "Extracted " + filepath + " to " + target

def main(args):
    parser = OptionParser(usage="python %prog tar_bz2_directory target_directory", version="%prog 1.0")
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Invalid number of arguments.")
    answer = raw_input("Do you want to extract all tar.bz2 files at " + args[0] + " to " + args[1] + " (yes/no)? ")
    if answer.strip() == "yes":
        extract(args[0], args[1])

main(sys.argv[1:])
