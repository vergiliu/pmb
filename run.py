from filecmp import dircmp
import sys
import logging
from FolderComparator import FolderComparator

FORMAT = '%(funcName)-20s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('starting up')
    l = sys.argv[1]
    r = sys.argv[2]

    fc = FolderComparator(l, r)
    fc.run_comparison()

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