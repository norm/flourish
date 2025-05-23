import pytest
import warnings

from flourish import Flourish

from .compare_directories import CompareDirectories


class FullGeneration(CompareDirectories):
    expected_directory = 'tests/output'
    expected_files = [
        '2015/12/25/index.html',
        '2015/12/index.html',
        '2015/index.html',
        '2016/02/29/index.html',
        '2016/02/index.html',
        '2016/06/04/index.html',
        '2016/06/06/index.html',
        '2016/06/index.html',
        '2016/index.html',
        '404.html',
        'all/index.html',
        'all/page-2.html',
        'archives.html',
        'basic-page.html',
        'css/debug.css',
        'css/screen.css',
        'error.html',
        'images/an-image.jpg',
        'index.atom',
        'index.csv',
        'index.html',
        'logo.png',
        'markdown-page.html',
        'nope.txt',
        'nothing.html',
        'series/index.html',
        'series/part-one.html',
        'series/part-three.html',
        'series/part-two.html',
        'tags/basic-page/basic-page.html',
        'tags/basic-page/index.atom',
        'tags/basic-page/index.html',
        'tags/basically/index.atom',
        'tags/basically/index.html',
        'tags/basically/thing-one.html',
        'tags/basically/thing-two.html',
        'tags/first/index.atom',
        'tags/first/index.html',
        'tags/first/thing-one.html',
        'tags/index/index.atom',
        'tags/index/index.html',
        'tags/index/series/index.html',
        'tags/one/index.atom',
        'tags/one/index.html',
        'tags/one/series/part-one.html',
        'tags/one/thing-one.html',
        'tags/second/index.atom',
        'tags/second/index.html',
        'tags/second/thing-two.html',
        'tags/series/index.atom',
        'tags/series/index.html',
        'tags/series/series/index.html',
        'tags/series/series/part-one.html',
        'tags/series/series/part-three.html',
        'tags/series/series/part-two.html',
        'tags/three/index.atom',
        'tags/three/index.html',
        'tags/three/series/part-three.html',
        'tags/two/index.atom',
        'tags/two/index.html',
        'tags/two/series/part-two.html',
        'tags/two/thing-two.html',
        'thing-one.html',
        'thing-two.html',
    ]


class TestFlourishGeneration(FullGeneration):
    def test_generation(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
                sass_dir='tests/sass',
                output_dir=self.tempdir,
            )

        with pytest.warns(UserWarning) as record:
            # one template has an invalid url() use
            flourish.generate_site()
            assert len(record) == 1
            assert 'tags-tag-page' in str(record[0].message)

        self.compare_directories()


class TestSectileTemplatesGeneration(FullGeneration):
    def test_generation(self):
        with pytest.warns(UserWarning) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                fragments_dir='tests/fragments',
                sass_dir='tests/sass',
                output_dir=self.tempdir,
            )

        with pytest.warns(UserWarning) as warnings:
            # one template has an invalid url() use
            flourish.generate_site()
            assert len(warnings) == 1
            assert 'tags-tag-page' in str(warnings[0].message)

        self.compare_directories()


class TestSinglePathGeneration(CompareDirectories):
    expected_directory = 'tests/paths'
    expected_files = [
        'index.html',
        'tags/first/index.atom',
        'tags/first/index.html',
        'tags/first/thing-one.html',
    ]

    def test_generation(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
                output_dir=self.tempdir,
            )

        flourish.generate_path('/')
        flourish.generate_path('/tags/first/?')
        self.compare_directories()
