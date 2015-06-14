import stat
import filecmp

class FolderComparator(filecmp.dircmp):
    def __init__(self, left, right, ignore=None, hide=None):
        super().__init__(left, right, ignore, hide)

        # self.left = left
        # self.right = right

    def run_comparison(self):
        self.report()
