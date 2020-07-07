from shutil import rmtree
from tempfile import mkdtemp

from flourish.lib import relative_list_of_files_in_directory


class CompareDirectories:
    def setup_method(self, meth):
        self.tempdir = mkdtemp()

    def teardown_method(self, meth):
        rmtree(self.tempdir)

    def compare_directories(self):
        tested_files = relative_list_of_files_in_directory(self.tempdir)
        assert sorted(tested_files) == sorted(self.expected_files)

        for filename in self.expected_files:
            self.compare_file(filename)

    def compare_file(self, filename):
        expected_file = '%s/%s' % (self.expected_directory, filename)
        tested_file = '%s/%s' % (self.tempdir, filename)
        with open(expected_file) as file:
            expected = file.read()
        with open(tested_file) as file:
            tested = file.read()

        assert tested == expected
