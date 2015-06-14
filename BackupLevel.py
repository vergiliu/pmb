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
