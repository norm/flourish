import os
from shutil import rmtree
from tempfile import mkdtemp


class CompareDirectories:
    def setup_method(self, meth):
        self.tempdir = mkdtemp()

    def teardown_method(self, meth):
        rmtree(self.tempdir)

    def compare_directories(self):
        tested_files = []
        trim = len(self.tempdir) + 1
        for root, dirs, files in os.walk(self.tempdir):
            this_dir = root[trim:]
            for file in files:
                if len(this_dir):
                    file = '%s/%s' % (this_dir, file)
                tested_files.append(file)

        assert sorted(self.expected_files) == sorted(tested_files)

        for filename in self.expected_files:
            self.compare_file(filename)

    def compare_file(self, filename):
            expected_file = '%s/%s' % (self.expected_directory, filename)
            tested_file = '%s/%s' % (self.tempdir, filename)
            with open(expected_file) as file:
                expected = file.read()
            with open(tested_file) as file:
                tested = file.read()

            assert expected == tested
