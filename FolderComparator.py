import os
import shutil
import stat
import filecmp
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class BackupLevel:
    """There are 3 main configurations, depending on what we want to achieve
    backup(0) is to copy all new/different files from the current location to the backup location
    restore(1) is to restore all/different files from the backup location to the current location
    both(2) is to have all files in both locations, and depending on another* option to choose one of them
    *another* to be decided - by date, by type, by file_size, by other things
    """
    backup = 0
    restore = 1
    both = 2


class FolderComparator(filecmp.dircmp):
    def __init__(self, source, destination, ignore=None, hide=None, mode=BackupLevel.backup):
        super().__init__(source, destination, ignore, hide)
        self.left = source
        self.right = destination
        self.mode = mode

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
        # todo sync_method should come from class
        for a_file in sub_folder:
            my_file_path = os.path.realpath(os.path.join(self.left, a_file))
            logger.info('\t{} '.format(my_file_path))
            logger.debug('\t {} -> {}'.format(os.path.realpath(self.left), os.path.realpath(self.right)))
            # shutil.copy2()
            if sync_method == BackupLevel.backup:
                logger.info('copy')
            elif sync_method == BackupLevel.restore:
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
