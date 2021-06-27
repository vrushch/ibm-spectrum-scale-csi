import os
import sys
import time
import shutil
import logging
import threading
import subprocess
import argparse
from datetime import datetime
from checksumdir import dirhash

io_suffix = 'io_dir'
hlink_suffix = 'hlink_dir'
slink_suffix = 'slink_dir'
footprint_file = 'iotool.checksum'
fio_suffix = 'fio_dir'

progress = u'\u2799'
correct = u'\u2713'
wrong = u'\u2715'

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def print_with_timestamp(text, end="\n"):

    now = datetime.now()
    d, t = now.date(), now.time()
    print(d, t, text, end=end)
#    num = len(args)
#    argstr = "{}"*num
#    print(d, t, argstr.format(args))


def banner(text):

    print("=====================")
    print(f"{text}")
    print("=====================")


def banner_create_files(files, filesize, depth, breadth, files_per_directory):

    total_dirs = breadth * depth

    print("Script will create:")
    print(f"| #####################################################")
    print(f"| Top/Breadth level dirs               : {breadth}")
    print(f"| Nested/Depth dirs per Top level dirs : {depth}")
    print(f"| Total dirs (Breadth * Depth)         : {total_dirs}")
    print(f"| Total files                          : {files}")
    print(f"| Files per directory                  : {files_per_directory}")
    print(f"| Filesize                             : {filesize}")
    print(f"| #####################################################")
    print()
    time.sleep(5)


def print_final_result(test_result):

    #print("##########################################")
    #print("        TEST RESULT ")
    print("##########################################")
    test_id = 1
    failed_tests = 0
    for test, result in test_result.items():
        #result = "PASS" if result else "FAIL"
        if result:
            result = "PASS"
        else:
            result = "FAIL"
            failed_tests += 1
        print("{:3d}. {:20} => {:5}".format(test_id, test, result))
        test_id += 1
    final_result = "FAILED" if failed_tests else "PASSED"
    print("##########################################")
    print(f"TEST RESULT is {final_result}")
    print("##########################################")

    return failed_tests

def get_free_space(testdir):

    stat = shutil.disk_usage(testdir)

    free_space_in_gb = stat.free // 2**30

    return free_space_in_gb


def is_filesize_correct(filesize):

    digits, unit = filesize[:-1], filesize[-1]

    possible_units = ('K', 'M', 'G')

    if digits.isdigit() and unit.endswith(possible_units):
        return True
    else:
        return False


def get_size_units(filesize):

    size, unit = filesize[:-1], filesize[-1]

    unit_to_size = {
            'K': 1024,
            'M': 1048576, #1024 * 1024
            'G': 1073741824, #1024 * 1024 * 1024
    }

    return int(size), unit_to_size[unit]


def get_bs_count_for_dd_command(filesize):
    """set bs=1024, count=filesize/1024"""

    size, count = get_size_units(filesize)

    bs, count = 1024, (size * count)//1024

    return bs, count

def create_file(filepath, bs=1, count=1):
    """create a file

    return:
    True - if command succeeds
    False - if command fails
    """

    if bs < 1 or count < 1:
        print("Invalid values for bs= and count= options.")
        print("bs >= 1, count >= 1")
        return False

    cmd = f"dd if=/dev/urandom of={filepath} bs={bs} count={count} > /dev/null 2>&1"

    #rc = os.system(cmd)
    rc = subprocess.call(cmd, shell=True)

    return rc == 0


def print_progress_bar(event):
    """print progress bar when checksum calculation is in progress."""

    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        event.wait(0.5)

        if event.is_set():
            break


def get_dir_md5hash(directory, excluded_files=None):
    """get checksum of directory"""

    print(f"\nfind checksum for directory {directory}")
    print("This step may take a while depending on the size of directory.")
    print("Please wait (directory checksum calculation in progress)...")
    start = time.time()

    #calculate checksum takes time, hence I wanted to show progress bar so that
    #user doesn't feel script is hanging due to stalled console
    #hence the below code for depicting progress bar while calculating checksum.
    event = threading.Event()
    progress_thread = threading.Thread(target=print_progress_bar, args=(event,))
    progress_thread.start()

    md5hash = dirhash(directory, 'md5', excluded_files=[excluded_files])
    event.set()
    progress_thread.join() # stop progress_thread from printing progress bar henceforth

    end = time.time()
    print(f"\nchecksum for directory {directory} is: {md5hash}\n")
    print("Took ", round(end-start, 2), "seconds to calculate checksum for directory")

    return md5hash


def is_space_available(testdir, files, filesize, depth, breadth):
    """verify system has sufficient space to create data."""

    print("verify system has sufficient space to create data")
    
    size, count = get_size_units(filesize)

    required_space = (files * size * count) // (2**30) #in GB

    free_space = get_free_space(testdir) #in GB

    print(f"Required space  : {required_space}GB")
    print(f"Available space : {free_space}GB")

    if required_space < free_space:
        print(f"{correct} enough space available. Ready to go.\n")
        return True
    else:
        print(f"{wrong} space crunch. Stopping here.\n")
        return False

def test_create_files_singleton(testdir, files, filesize, depth, breadth):
    """create files with nested directory structure (if requested)"""

    banner("start: test create files")
    
    if not is_space_available(testdir, files, filesize, depth, breadth):
        return False

    test_result = True

    #calculate files to create per directory
    files_per_directory = files // (depth * breadth)

    banner_create_files(files, filesize, depth, breadth, files_per_directory)

    #calculate bs size for dd command
    #bs, count = get_size_units(filesize)
    bs, count = get_bs_count_for_dd_command(filesize)

    #create string for nested directory structure
    nested_dirs = ""
    if depth > 1:
        for i in range(1,depth+1):
            nested_dirs += f'{os.path.sep}{i}'
        #print(nested_dirs)

    #create main directory e.g. test/io_dir/
    io_dir = f"{testdir}/{io_suffix}"

    #create dirs for breadth parameter e.g. test/io_dir/d1 , test/io_dir/d2
    top_level_dirs = [f"d{i}" for i in range(1,breadth+1)]

    #create dirs under each breadth/top level dir
    for top_level_dir in top_level_dirs:

        #create nested directory structure
        os_walk_dir = f"{io_dir}/{top_level_dir}"  # test/io_dir/d1/
        os.makedirs(f"{os_walk_dir}/{nested_dirs}") # test/io_dir/d1/1/2/3/...

        #create files inside each nested directory
        print(f"Creating files in {top_level_dir}", end="")
        for dirpath, dirnames, filenames in os.walk(os_walk_dir):

            #do not create files directly inside top level directory
            #start creating files inside nested directories
            if dirpath == os_walk_dir:
                continue

            print(".", end="")
            logger.info(f"{dirpath}...")
            for filename in range(1,files_per_directory+1):
                filepath = os.path.join(dirpath, f"f{filename}")
                file_created = create_file(filepath, bs=bs, count=count)
                test_result &= file_created #ensure each file create succeeds
                logger.info(f"File {filepath} created : {file_created}")
        print()

    print("\n*** create files test completed. ***\n")

    return test_result

def test_create_files_with_threads(testdir, files, filesize, depth, breadth):
    """create files with nested directory structure (if requested)"""

    banner("start: test_create_files test")
    
    if not is_space_available(testdir, files, filesize, depth, breadth):
        return False

    test_result = True

    #calculate files to create per directory
    files_per_directory = files // (depth * breadth)

    banner_create_files(files, filesize, depth, breadth, files_per_directory)

    #calculate bs size for dd command
    #bs, count = get_size_units(filesize)
    bs, count = get_bs_count_for_dd_command(filesize)

    #create string for nested directory structure
    nested_dirs = ""
    if depth > 1:
        for i in range(1,depth+1):
            nested_dirs += f'{os.path.sep}{i}'
        #print(nested_dirs)

    #create main directory e.g. test/io_dir/
    io_dir = f"{testdir}/{io_suffix}"

    #create dirs for breadth parameter e.g. test/io_dir/d1 , test/io_dir/d2
    top_level_dirs = [f"d{i}" for i in range(1,breadth+1)]

    threads = []

    #create dirs under each breadth/top level dir
    for top_level_dir in top_level_dirs:

        thr_args = (io_dir, top_level_dir, nested_dirs, files_per_directory, bs, count)
        thread = threading.Thread(target=thread_task, args=thr_args)
        threads.append(thread)

    print("\n === starting all threads (Each thread creates one top/breadth level directory) ... ===\n")
    for thread in threads:
        thread.start()

    time.sleep(2) #giving a chance to let all threads print that they started

    print("\n === waiting for all threads to finish ... ===\n")
    for thread in threads:
        thread.join()

    banner("create files test completed.")

    return test_result


#def thread_task(thr_args=None):
#    io_dir, top_level_dir, nested_dirs, files_per_directory, bs, count = thr_args

def thread_task(io_dir, top_level_dir, nested_dirs, files_per_directory, bs, count):
    """create files in one top/breadth level directory"""

    #thread name
    thread_name = threading.currentThread().getName()

    #create nested directory structure
    os_walk_dir = f"{io_dir}/{top_level_dir}"  # test/io_dir/d1/
    os.makedirs(f"{os_walk_dir}/{nested_dirs}") # test/io_dir/d1/1/2/3/...

    #create files inside each nested directory
    print(f"{progress} {thread_name} started - Creating files in {top_level_dir}")
    for dirpath, dirnames, filenames in os.walk(os_walk_dir):

        #do not create files directly inside top level directory
        #start creating files inside nested directories
        if dirpath == os_walk_dir:
            continue

        #print(".", end="")
        logger.info(f"{dirpath}...")
        for filename in range(1,files_per_directory+1):
            filepath = os.path.join(dirpath, f"f{filename}")
            file_created = create_file(filepath, bs=bs, count=count)
            #test_result &= file_created #ensure each file create succeeds
            logger.info(f"File {filepath} created : {file_created}")
    #print(f"Thread {thread_name} finished - Creating files in {top_level_dir}")
    print(f"{correct} {thread_name} finished - Creating files in {top_level_dir}")


def create_test_setup(suffix_dir):

    #create test directory to test io/hardlinks/symlinks
    os.makedirs(f"{suffix_dir}")

    #create source file
    print("Create source file in suffix_dir")
    source_file = os.path.join(suffix_dir, "source_file")
    file_created = create_file(source_file)
    if file_created:
        logger.info(f"PASS: Source File {source_file} created.")
        return True
    else:
        logger.error(f"FAIL: Source File {source_file} creation failed.")
        return False


def test_create_filetypes(testdir, ftype):
    """create hardlinks/symlinks

    1. create a source file
    2. create 100 hardlinks/sym links to source file based on input 'ftype'
    """

    banner(f"start: create {ftype} test")
    
    symlink_dir = f"{testdir}/{slink_suffix}"
    hardlink_dir = f"{testdir}/{hlink_suffix}"

    if ftype == 'symlink' : suffix_dir = symlink_dir
    if ftype == 'hardlink': suffix_dir = hardlink_dir

    #create test setup for testing symlinks
    if not create_test_setup(suffix_dir):
        print("creating test setup for testing {ftype} failed.")
        return False

    print(f"Create {ftype} to source_file")

    cwd = os.getcwd()
    os.chdir(suffix_dir)
    source_file = 'source_file'
    #source_file = os.path.join(suffix_dir, 'source_file')

    for filename in range(1,101):
        print(".", end="")

        #dest_file = os.path.join(suffix_dir, f"f{filename}")
        dest_file = f"f{filename}" #e.g. f1, f2, ..., f100
        try:
            if ftype == 'symlink':
                os.symlink(source_file, dest_file)
            elif ftype == 'hardlink':
                os.link(source_file, dest_file)
        except OSError as error:
            banner(f"FAIL: Failed to create {ftype}. Got exception:\n{error}")
            os.chdir(cwd)
            return False
    print()
    os.chdir(cwd)
    #for hardlink, ensure all files created share common inode number
    if ftype == 'hardlink' and not test_check_hardlinks(testdir):
        banner(f"FAIL: Failed to create {ftype}. Inode numbers didn't match for all files.")
        return False

    print(f"\n*** PASS: create {ftype} test passed. ***\n")
    return True


def generate_data(mntdir, testdir, files, filesize, depth, breadth, thr_flag):

    test_result = {
        'create files': False,
        #'create hardlinks' : False,
        'create symlinks': False
    }

    testdir = os.path.join(mntdir, testdir)
    if os.path.exists(testdir):
        print(f"{testdir} directory is already created. Tool won't wipe it out.")
        sys.exit(1)
    else:
        os.makedirs(testdir)

    #################
    # data generation
    #################
    #1) create files
    if thr_flag:
        result = test_create_files_with_threads(testdir, files, filesize, depth, breadth)
    else:
        result = test_create_files_singleton(testdir, files, filesize, depth, breadth)
    test_result['create files'] = result

    #2) create hardlinks
    #result = test_create_filetypes(testdir, 'hardlink')
    #test_result['create hardlinks'] = result

    #3) create symlinks
    result = test_create_filetypes(testdir, 'symlink')
    test_result['create symlinks'] = result

    #4) create filenames with special characters
    #compressed files, chr device, blk device, image, zip, socket
    #5) create files with special characters as data

    #################
    # checksum calculation
    #################

    #find out checksum for entire testdir and store it in a file
    #this file will be used later to confirm copy/restore succeeds
    dir_md5hash = get_dir_md5hash(testdir)

    footprint_filepath = f"{testdir}/{footprint_file}"
    with open(footprint_filepath, 'w') as f:
        f.write(dir_md5hash)

    logger.info("==================")
    logger.info(f"checksum is {dir_md5hash}")
    logger.info("==================")

    #return dir_md5hash
    return print_final_result(test_result)


def test_check_checksum(testdir, checksum=None):

    banner("start: check checksum test")
    actual_dir_md5hash = get_dir_md5hash(testdir, excluded_files=footprint_file)

    if not checksum:
        footprint_filepath = f"{testdir}/{footprint_file}"
        with open(footprint_filepath) as f:
            checksum = f.read()

    print(f"Actual checksum   : {actual_dir_md5hash}")
    print(f"Expected checksum : {checksum}\n")

    if actual_dir_md5hash == checksum:
        print("\n*** PASS: Checksum matched. ***\n")
        return True
    else:
        banner("\n*** FAIL: Checksum mismatch. ***\n")
        return False


def test_check_hardlinks(testdir):
    """verify all files in hlink_suffix directory have common inode"""

    banner("start: check hardlinks test")

    unique_inodes = set()

    #read inode numbers for all files in hardlink_dir
    hardlink_dir = f"{testdir}/{hlink_suffix}"
    files = os.listdir(hardlink_dir)
    for fname in files:
        dest_file = os.path.join(hardlink_dir, fname)
        fname_inode = os.stat(dest_file).st_ino
        unique_inodes.add(fname_inode)
        logger.info(f"file {fname}, inode number {fname_inode}")

    #if each file has same inode number, then unique_inodes() set will contain only one element
    print(unique_inodes)
    if len(unique_inodes) == 1:
        message = f"PASS: All files have same inode number {unique_inodes} in directory {hardlink_dir}."
        print("\n***", message, " ***\n")
        return True
    else:
        message = f"FAIL: All files don't have same inode number. The inode numbers found are {unique_inodes}."
        print("\n***", message, " ***\n")
        return False


def test_check_symlinks(testdir):
    """verify all files in hlink_suffix directory have common inode"""

    banner("start: check symlinks test")

    unique_inodes = set()

    #read inode numbers for all files in hardlink_dir
    symlink_dir = f"{testdir}/{slink_suffix}"
    files = os.listdir(symlink_dir)
    for fname in files:
        if fname == 'source_file': #skip 'source_file', this is not symlink
            continue
        fname = f"{symlink_dir}/{fname}"
        if not os.path.islink(fname): #return immediately, if any other file is not symlink
            print(f"\n*** symlink check failed: {fname} is not symlink. ***\n")
            return False

    print(f"\n*** symlink check passed. ***\n")
    return True


def validate_data(mntdir, testdir, checksum=None):

    #banner("start: validate_data test")

    test_result = {
        'check files': False,
        #'check hardlinks' : False,
        'check symlinks': False
    }
    
    testdir = os.path.join(mntdir, testdir)
    if not os.path.exists(testdir):
        print(f"{testdir} doesn't exist to validate.")
        sys.exit(1)

    #################
    # data validation
    #################
    #1) checksum validation (checksum of original and destination directory should match)
    result = test_check_checksum(testdir, checksum=None)
    test_result['check files'] = result

    #2) check hardlinks
    #result = test_check_hardlinks(testdir)
    #test_result['check hardlinks'] = result

    #3) create symlinks
    result = test_check_symlinks(testdir)
    test_result['check symlinks'] = result

    #4) create filenames with special characters

    #5) create files with special characters as data

    return print_final_result(test_result)

#######################
#fio tests
#######################


def is_cmd_available(cmd):
    """verify if command/executable is installed"""

    return True if shutil.which(cmd) else False


def get_fio_command(io_pattern, directory,
        bs="4k", filesize="512M", numjobs=20, runtime=20):
    """form fio command to run

    Reference link: https://fio.readthedocs.io/en/latest/fio_doc.html

    - running fio with blocksize (bs=4k) for total size of (size=512M) against
      destination directory (directory=XXXXX) with 20 jobs/threads (numjobs=20).
    - fio command will run for 30 seconds (runtime=30).
    - minimal output is captured using --group-reporting
    - this script aims to use fio for data generation activity and not for
      measuring io statistics, hence using --output-format=normal.
      --output-format=json is useful to parse/operate resulting i/o stats.
    """

    #fio --name=randwrite --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --direct=0 --size=16M --numjobs=20 --runtime=30 --group_reporting --time_based --directory=d1

    cmd = f"fio --name={io_pattern} --ioengine=libaio --rw={io_pattern} \
            --bs={bs} --size={filesize}M --numjobs={numjobs} \
            --runtime={runtime} --time_based --directory={directory} \
            --group_reporting --output-format=normal"

    return cmd


def execute_fio(testdir, io_pattern):
    """execute fio command for an input io_pattern"""

    banner(f"Running fio for {io_pattern} I/O Pattern...")

    fio_dir = f"{testdir}/{fio_suffix}/{io_pattern}"
    os.makedirs(f"{fio_dir}")

    fio_cmd = get_fio_command(io_pattern, fio_dir)

    rc = subprocess.call(fio_cmd, shell=True)

    return rc == 0


def test_fiowrite(mntdir, testdir):
    """call execute_fio() for various io_patterns"""

    print("""This test will create data using fio tool.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    - various i/o patterns will be used e.g. sequential/random read/write.
    - Each i/o pattern will read/write max 512M data using 4k block size.
    - Each i/o pattern will run for 30 seconds. We've 6 i/o patterns/
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """)

    time.sleep(5)

    io_patterns = [
            'read',          # sequential read
            'write',         # sequential write
            'randread',      #random reads
            'randwrite',     #random writes
            'readwrite',     #sequential mixed reads and writes
            'randrw',        #random mixed reads and writes
    ]

    #define test cases (6 tests - 1 for each io_pattern)
    test_result = {f"test {i}": False for i in io_patterns}

    #verify we are not over-writing existing directory
    testdir = os.path.join(mntdir, testdir)
    if os.path.exists(testdir):
        print(f"{testdir} directory is already created. Tool won't wipe it out.")
        sys.exit(1)
    os.makedirs(f"{testdir}")

    #execute fio write tests for various i/o patterns and store test result
    for io_pattern in io_patterns:
        test_name = f"test {io_pattern}"
        test_result[test_name] = execute_fio(testdir, io_pattern)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("fio write using i/o patterns finished.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    #################
    # checksum calculation
    #################

    #find out checksum for entire testdir and store it in a file
    #this file will be used later to confirm copy/restore succeeds
    dir_md5hash = get_dir_md5hash(testdir)

    footprint_filepath = f"{testdir}/{footprint_file}"
    with open(footprint_filepath, 'w') as f:
        f.write(dir_md5hash)

    print(f"fiowrite directory checksum is {dir_md5hash}")

    return print_final_result(test_result)


def test_fiocheck(mntdir, testdir, checksum=None):
    """verify fiowrite directory checksum and mntdir/testdir checksum is equal"""

    test_result = {
        'check fio': False,
    }
 
    testdir = os.path.join(mntdir, testdir)
    if not os.path.exists(testdir):
        print(f"{testdir} doesn't exist to validate.")
        sys.exit(1)

    result = test_check_checksum(testdir, checksum=None)
    test_result['check fio'] = result

    return print_final_result(test_result)


def set_default(files, filesize, depth, breadth):

    #set default if missing
    if not files:    files    = 10
    if not filesize: filesize = '1M'
    if not depth:    depth    = 2
    if not breadth:  breadth  = 1

    return files, filesize, depth, breadth


def main():
    # parse agruments using argparse module
    # -f/--file is a mandatory argument, -s/--stanza and -a/--attribute are optional arguments
    parser = argparse.ArgumentParser(
                description='------- script to generate and validate i/o.',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="""
examples:
        1) create/generate data e.g. total 1000 files in 50 directories, plus hardlinks and symlinks
           
           python3 iotool.py write /mnt/fs1/fset1 dir1 --files 1000 --filesize 1M --depth 5 --breadth 10

        2) suppose one takes snapshot of /mnt/fs1/fset1/dir1 or copies it elsewhere
           (e.g. cp -R /mnt/fs1/fset1/dir1 /mnt/fs2/fset2/dir2)
           then, copied/restored data can be checked as below

           python3 iotool.py check /mnt/fs2/fset2 dir2

        3) fio tool - generate different i/o pattern data (e.g. sequential/random read/write)

           python3 -u iotool.py fiowrite /mnt/fs1/fset1 dir1

        4) suppose one takes snapshot of /mnt/fs1/fset1/dir1 and restores it to /mnt/fs2/fset2/dir2
           then, validate the restored snapshot data of fio tool as below:

           python3 iotool.py fiocheck /mnt/fs2/fset2 dir2
              """)
    parser.add_argument("operation", choices=['write', 'check', 'fiowrite', 'fiocheck'],)
    parser.add_argument("mntdir", help="mount path")
    parser.add_argument("testdir", help="create this directory under mount path")
    parser.add_argument("--checksum", help="checksum to compare with")
    parser.add_argument("--files", type=int, help="total number of files to create")
    parser.add_argument("--filesize", help="size of each file e.g. 1M, 1G, 100K")
    parser.add_argument("--depth", type=int, help="number of nested directories to create")
    parser.add_argument("--breadth", type=int, help="number of top level directories to create")
    parser.add_argument("--threads", action='store_true')
    args = parser.parse_args()

    operation = args.operation
    mntdir = args.mntdir
    testdir = args.testdir
    checksum = args.checksum #if user explicitly provides checksum of directory
    thr_flag = args.threads
    (files, filesize, depth, breadth) = set_default(args.files, args.filesize, args.depth, args.breadth)

    #verify mntdir is valid directory
    if not os.path.isdir(mntdir):
        print(f"Test path {mntdir} is not a directory. Please provide a directory to test.")
        sys.exit(1)

    #run checks for filesize
    if filesize:
        if not is_filesize_correct(filesize):
            print(f"Incorrect filesize {filesize} provided. It should be e.g. 1M, 1G, 100K")
            sys.exit(1)

    #possible options - write, check, fio
    if operation == 'write':
        rc = generate_data(mntdir, testdir, files, filesize, depth, breadth, thr_flag)
    elif operation == 'check':
        rc = validate_data(mntdir, testdir, checksum)
    elif operation in ('fiowrite', 'fiocheck'):
        if not is_cmd_available('fio'):
            print("fio tool is not installed. Hence not running fio tests.")
            print("how to install fio? - yum/apt-get install fio")
            rc = 1
        elif operation == 'fiowrite':
            rc = test_fiowrite(mntdir, testdir)
        elif operation == 'fiocheck':
            rc = test_fiocheck(mntdir, testdir, checksum)

    sys.exit(rc)


if __name__ == '__main__':
    try:
        main()
        #get_dir_md5hash('test2/ganesha')
        #get_dir_md5hash('r/ganesha')
    except Exception as e:
        print(f"Exception while executing the script\n{e}")

