import os
import stat
import filecmp
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

class FolderComparator(filecmp.dircmp):
    def __init__(self, source, destination, ignore=None, hide=None):
        super().__init__(source, destination, ignore, hide)
        self.left = source
        self.right = destination

    def print_current_state(self):
        logger.info('Checking folders [{}] vs [{}]'.format(self.left, self.right))
        self.check_root_diffs()
        self.run_comparison(self.subdirs.values())

    def run_comparison(self, folders):
        for sub_folder in folders:
            if sub_folder.diff_files:
                logger.info('Diff {}'.format(sub_folder.diff_files))
                self.check_single_file(sub_folder.diff_files)
            if sub_folder.left_only:
                logger.info('new {}'.format(sub_folder.left_only))
                self.check_single_file(sub_folder.left_only)
            if sub_folder.right_only:
                logger.info('old {}'.format(sub_folder.right_only))
                self.check_single_file(sub_folder.right_only)
            if sub_folder.subdirs:
                logger.info('')
                self.run_comparison(sub_folder.subdirs.values())

    def check_single_file(self, sub_folder):
        for a_file in sub_folder:
            logger.info(os.path.realpath(a_file))

    def check_root_diffs(self):
        if self.left_only:
            logger.info('New {}'.format(self.left_only))
            self.check_single_file(self.left_only)
        if self.right_only:
            logger.info('Old {}'.format(self.right_only))
            self.check_single_file(self.right_only)
