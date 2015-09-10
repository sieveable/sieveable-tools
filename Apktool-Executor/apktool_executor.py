#!/usr/bin/python
import sys
import os
import datetime
import logging
import multiprocessing
from multiprocessing import Pool
from optparse import OptionParser
from subprocess import Popen, PIPE
from version import __version__
import ConfigParser


log = logging.getLogger("apktool_executor")
log.setLevel(logging.DEBUG) # The logger's level must be set to the "lowest" level.
config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         "config.conf"))
aapt_path = config.get('tools', 'aapt')
apktool_path = config.get('tools', 'apktool')

# pickled method defined at the top level of a module to be called by multiple processes.
# Runs apktool and returns the directory of the unpacked apk file.
def run_apktool(apk_file, target_dir, framework_dir, tag, no_src, no_res):
    log.info("Running apktool on " + apk_file)
    apk_name = os.path.basename(os.path.splitext(apk_file)[0])
    target_dir = os.path.join(target_dir, apk_name)
    apk_version_info = get_apk_info(apk_file)
    # skip the target directory if it already exists
    if os.path.exists(target_dir):
        log.warn("Target directory already exists")
        return None, None
        
    args = [apktool_path, 'd', apk_file, '-o', target_dir]
    if framework_dir:
        args.append('-p')
        args.append(framework_dir)
    elif tag:
        args.append('-t')
        args.append(tag)
    elif no_src:
        args.append('-s')
    elif no_res:
        args.append('-r')
    sub_process = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = sub_process.communicate()
    rc = sub_process.returncode
    if rc == 0:
        log.info(out)
    if rc != 0:
        log.error('Failed to decode apk file: ' + apk_file + '\n' + err)
        return None, None
    return target_dir, apk_version_info


# Returns a tuple containing the package, version code, and version name.
def get_apk_info(apk_path):
    try:
        sub_process = Popen([aapt_path, 'dump', 'badging', apk_path], stdout=PIPE, stderr=PIPE)
        out, err = sub_process.communicate()
    except OSError:
        print('Error: aapt tool is not defined in the config file at: ./config/tools.conf')
        sys.exit(-1)
    version_info = {}
    if out:
        for line in out.split('\n'):
            segment = line.strip().split(":")
            if segment is not None and len(segment) > 0:
                if segment[0] == "package":
                    package_info = segment[1].strip().split(' ')
                    for info_line in package_info:
                        info = info_line.strip().split('=')
                        if info[0] == "name":
                            version_info['name'] = info[1].replace("'", "")
                        elif info[0] == 'versionCode':
                            version_info['version_code'] = info[1].replace("'", "")
                        elif info[0] == 'versionName' :
                            version_info['version_name'] = info [1].replace("'", "")
                    break
    # Return a hash of version code and version name
    return version_info


class ApktoolExecutor(object):
    # Set the number of worker processes to the number of available CPUs.
    processes = multiprocessing.cpu_count()

    def __init__(self):
        self.apk_files = []
        self.framework_dir = None
        self.tag = None
        self.no_src = False
        self.no_res = False
            
    def start_main(self, path_file, target_dir):
        apk_paths = []
        # Create pool of worker processes
        pool = Pool(processes=self.processes)
        log.info('A pool of %i worker processes has been created', self.processes)

        # If the apk path file is given
        with open(path_file, 'r') as f:
            for line in f:
                line = line.strip()
                if os.path.exists(line):
                    apk_paths.append(line)
                else:
                    log.error('No such file: %s', line)

        if len(apk_paths) > 0:
            try:
                # Run apktool on the apk file asynchronously.
                results = [pool.apply_async(run_apktool,
                                            (apk_path, target_dir,
                                             self.framework_dir, self.tag,
                                             self.no_src, self.no_res))
                           for apk_path in apk_paths]
                for r in results:
                    if r is not None:
                        target_dir, apk_version_info = r.get()
                        if not target_dir or not apk_version_info:
                            continue
                        apktool_file = os.path.join(target_dir, 'apktool.yml')
                        if not os.path.exists(apktool_file):
                            self.write_version_to_apktoolyml(apktool_file, 
                                                             apk_version_info)
                        log.info("APK file has been extracted at: " + target_dir)
                # close the pool to prevent any more tasks from being 
                # submitted to the pool.
                pool.close()
                # Wait for the worker processes to exit
                pool.join()
            except KeyboardInterrupt:
                print('got ^C while worker processes have outstanding work. '''
                      'Terminating the pool and stopping the worker processes'''
                      ' immediately without completing outstanding work..')
                pool.terminate()
                print('pool has been terminated.')
        else:
            log.error('Failed to find apk files in %s', path_file)
                        
    @staticmethod
    def write_version_to_apktoolyml(apktool_file, version_info):
        with open(apktool_file, 'w') as f:
            f.write('versionInfo:\n')
            f.write("  versionCode: '" + version_info['version_code']+ "'\n")
            f.write("  versionName: " + version_info['version_name']+ "\n")
    
    @staticmethod
    # check apktool version.
    def check_apktool_version():
        sub_process = Popen(['apktool', '--version'], 
                            stdout=PIPE, stderr=PIPE)
        out, err = sub_process.communicate()
        if out:
            # Only accept version 2.0 or higher
            if int(out.strip().split('.')[0]) == 2:
                print('using apktool version ' + out.strip())
            else:
                raise Exception('Unsatisfied dependencies for apktool. ' + 
                                'Please install apktool version 2.0.0-Beta9 or higher. ' + 
                                'See the README file for additional information.')
        
    def main(self, argv):
        # check apktool version
        self.check_apktool_version()
        start_time = datetime.datetime.now()
        # Configure logging
        logging_file = None
        logging_level = logging.ERROR
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # Create console logger and set its formatter and level
        logging_console = logging.StreamHandler(sys.stdout)
        logging_console.setFormatter(formatter)
        logging_console.setLevel(logging.DEBUG)
        # Add the console logger
        log.addHandler(logging_console)
        
        # command line parser
        parser = OptionParser(usage="python %prog apk_path_file "
                             "target_directory [options]",
                              version="%prog " + __version__)
        parser.add_option("-p", "--processes", dest="processes", type="int",
                           help="the number of worker processes to use. " +
                           "Default is the number of CPUs in the system.")
        parser.add_option("-w", "--framework", help="forces apktool to use "
                          "framework files located in <FRAMEWORK_DIR>."
                          , dest="framework_dir")
        parser.add_option("-t", "--tag", help="forces apktool to use framework"
                          " files tagged by <TAG>.", dest="tag")
        parser.add_option("-s", "--no-src", help="Do not decode sources.",
                          dest="no_src", action='store_true', default=False)
        parser.add_option("-r", "--no-res", help="Do not decode resources.", 
                          dest="no_res", action='store_true', default=False)
        parser.add_option("-l", "--log", dest="log_file",
                          help="write logs to FILE.", metavar="FILE")
        parser.add_option('-v', '--verbose', dest="verbose", default=0,
                          action='count', help='increase verbosity.')
                          
        (options, args) = parser.parse_args(argv)
        if len(args) != 2:
            parser.error("incorrect number of arguments.")
        if options.processes:
            self.processes = options.processes
        if options.framework_dir:
            self.framework_dir = options.framework_dir
        if options.tag:
            self.tag = options.tag
        if options.no_src:
            self.no_src = True
        if options.no_res:
            self.no_res = True
        if options.log_file:
            logging_file = logging.FileHandler(options.log_file, mode='a',
                                               encoding='utf-8', delay=False)
            logging_file.setLevel(logging_level)
            logging_file.setFormatter(formatter)
            log.addHandler(logging_file)
        if options.verbose:
            levels = [logging.ERROR, logging.INFO, logging.DEBUG]
            logging_level = levels[min(len(levels) - 1, options.verbose)]
            
            # set the file logger level if it exists
            if logging_file:
                logging_file.setLevel(logging_level)

        path_file = None
        target_dir = None
        if os.path.isfile(args[0]):
            path_file = os.path.abspath(args[0])
        else:
            sys.exit("Error: apk path file " + args[0] + " does not exist.")
    
        if os.path.isdir(args[1]):
            target_dir = os.path.abspath(args[1])
        else:
            sys.exit("Error: target directory " + args[1] + " does not exist.")
    
        self.start_main(path_file, target_dir)
     
        print("======================================================")
        print("Finished after " + str(datetime.datetime.now() - start_time))
        print("======================================================")
    

if __name__ == '__main__':
    ApktoolExecutor().main(sys.argv[1:])
