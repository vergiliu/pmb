import sys
import logging
from BackupLevel import BackupLevel

from FolderComparator import FolderComparator

logging.basicConfig(format='%(asctime)s  %(funcName)-24s => %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('starting up')
    left = sys.argv[1]
    right = sys.argv[2]

    fc = FolderComparator(left, right)
    fc.synchronize_now()

    fc.print_queue()

    # NOW
    # find all files
        # left
        # right
    # compute differences
            # compare 2 files

    # NOT NOW
    # argparse
    # dedup
    # memory