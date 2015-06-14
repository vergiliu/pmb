import os
import stat
import filecmp
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class BackupLevel:
    backup = 0
    remove = 1
    both = 2


class FolderComparator(filecmp.dircmp):
    def __init__(self, source, destination, ignore=None, hide=None):
        super().__init__(source, destination, ignore, hide)
        self.left = source
        self.right = destination

    def print_current_state(self):
        logger.info('Checking folders [{}] vs [{}]'.format(self.left, self.right))
        logger.info('=' * 40)
        self.check_root_diffs()
        self.run_comparison(self.subdirs.values())

    def run_comparison(self, folders):
        for sub_folder in folders:
            if sub_folder.diff_files:
                logger.info('different files')
                self.sync_files_in_folder(sub_folder.diff_files)
            if sub_folder.left_only:
                logger.info('files to backup {}'.format(sub_folder.left_only))
                self.sync_files_in_folder(sub_folder.left_only)
            if sub_folder.right_only:
                logger.info('files present only on backup {}'.format(sub_folder.right_only))
                self.sync_files_in_folder(sub_folder.right_only)
            if sub_folder.subdirs:
                self.run_comparison(sub_folder.subdirs.values())

    def sync_files_in_folder(self, sub_folder, sync_method=BackupLevel.backup):
        for a_file in sub_folder:
            logger.info('\t{}'.format(os.path.realpath(a_file)))
            if sync_method == BackupLevel.backup:
                logger.info('copy')
            elif sync_method == BackupLevel.remove:
                logger.info('remove from backup')
            elif sync_method == BackupLevel.both:
                logger.info('both places')


    def check_root_diffs(self):
        if self.left_only:
            logger.info('files not present on backup')
            self.sync_files_in_folder(self.left_only)
        if self.right_only:
            logger.info('files present only on backup')
            self.sync_files_in_folder(self.right_only)
        if self.diff_files:
            logger.info('different root files')
            self.sync_files_in_folder(self.diff_files)
