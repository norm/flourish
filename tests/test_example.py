import os
import subprocess

from .compare_directories import CompareDirectories


class TestExample(CompareDirectories):
    expected_directory = 'tests/example'
    expected_files = [
        '2016/06.html',
        '2016/07.html',
        '2016/index.html',
        'adding-pages.html',
        'editing-the-site.html',
        'index.html',
        'site.css',
        'welcome.html',
    ]

    expected_templates = [
        'templates/base.html',
        'templates/homepage.html',
        'templates/index.html',
        'templates/page.html'
    ]
    expected_sources = [
        'source/_site.toml',
        'source/generate.py',
        'source/welcome.markdown',
        'source/editing-the-site.markdown',
        'source/adding-pages.markdown',
        'source/site.css'
    ]

    def test_flourish_example_command_and_output(self):
        result = subprocess.run(
            ['flourish', 'example'],
            cwd=self.tempdir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"flourish example failed with: {result.stderr}"

        for dir_name in ['source', 'templates', 'output']:
            dir_path = os.path.join(self.tempdir, dir_name)
            assert os.path.isdir(dir_path), f"Directory {dir_name} should be created"

        for file_path in self.expected_templates:
            full_path = os.path.join(self.tempdir, file_path)
            assert os.path.isfile(full_path), f"Template file {file_path} should be created"

        for file_path in self.expected_sources:
            full_path = os.path.join(self.tempdir, file_path)
            assert os.path.isfile(full_path), f"Source file {file_path} should be created"

        generate_result = subprocess.run(
            ['flourish', 'generate'],
            cwd=self.tempdir,
            capture_output=True,
            text=True,
        )
        assert generate_result.returncode == 0, f"flourish generate failed with: {generate_result.stderr}"

        self.compare_directories(input_dir=os.path.join(self.tempdir, 'output'))
