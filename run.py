import sys
import logging

from FolderComparator import FolderComparator

FORMAT = '%(funcName)-20s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('starting up')
    left = sys.argv[1]
    right = sys.argv[2]

    fc = FolderComparator(left, right)
    fc.print_current_state()

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