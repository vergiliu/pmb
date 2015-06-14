import os
import shutil
import stat
import filecmp
import logging
from BackupLevel import BackupLevel

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class FolderComparator(filecmp.dircmp):
    def __init__(self, source, destination, ignore=None, hide=None, method=BackupLevel.backup):
        super().__init__(source, destination, ignore, hide)
        self.left = source
        self.right = destination
        self.method = method

    def print_current_state(self):
        logger.info('Checking folders [{}] vs [{}]'.format(self.left, self.right))
        logger.info('=' * 40)
        self.check_root_diffs()
        self.run_comparison(self.subdirs.values())

    def run_comparison(self, folders):
        for sub_folder in folders:
            if sub_folder.left_only and (self.method == BackupLevel.backup or self.method == BackupLevel.both):
                logger.info('files to backup {}'.format(sub_folder.left_only))
                self.sync_files_in_folder(sub_folder.left_only, self.left, self.right)
            if sub_folder.right_only and (self.method == BackupLevel.restore or self.method == BackupLevel.both):
                logger.info('files present only on backup {}'.format(sub_folder.right_only))
                self.sync_files_in_folder(sub_folder.right_only, self.right, self.left)
            if sub_folder.diff_files:
                logger.info('different files')
                self.sync_files_in_folder(sub_folder.diff_files, self.left, self.right)
            if sub_folder.subdirs:
                self.run_comparison(sub_folder.subdirs.values())

    def sync_files_in_folder(self, sub_folder, from_folder, to_folder):
        for a_file in sub_folder:
            from_path = os.path.realpath(os.path.join(from_folder, a_file))
            to_path = os.path.realpath(os.path.join(to_folder, a_file))
            logger.debug('\n\t\t {} ->\n\t\t {}'.format(from_path, to_path))
            # shutil.copy2()
            if self.method == BackupLevel.backup:
                logger.info('copy')
            elif self.method == BackupLevel.restore:
                logger.info('remove from backup')
            elif self.method == BackupLevel.both:
                logger.info('both places')

    def check_root_diffs(self):
        if self.left_only and (self.method == BackupLevel.backup or self.method == BackupLevel.both):
            logger.info('files not present on backup')
            self.sync_files_in_folder(self.left_only, self.left, self.right)
        if self.right_only and (self.method == BackupLevel.both or self.method == BackupLevel.restore):
            logger.info('files present only on backup')
            self.sync_files_in_folder(self.right_only, self.right, self.left)
        if self.diff_files:
            logger.info('different root files')
            self.sync_files_in_folder(self.diff_files, self.left, self.right)
