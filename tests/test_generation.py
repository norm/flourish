import pytest

from flourish import Flourish

from .compare_directories import CompareDirectories


class TestFlourishGeneration(CompareDirectories):
    expected_directory = 'tests/output'
    expected_files = [
        '404.html',
        'all/index.html',
        'all/page-2.html',
        'basic-page.html',
        'css/screen.css',
        'error.html',
        'images/an-image.jpg',
        'index.atom',
        'index.html',
        'logo.png',
        'markdown-page.html',
        'nope.txt',
        'thing-one.html',
        'thing-two.html',
        'series/part-one.html',
        'series/part-three.html',
        'series/part-two.html',
        'tags/basic-page/index.atom',
        'tags/basic-page/index.html',
        'tags/basically/index.atom',
        'tags/basically/index.html',
        'tags/first/index.atom',
        'tags/first/index.html',
        'tags/one/index.atom',
        'tags/one/index.html',
        'tags/second/index.atom',
        'tags/second/index.html',
        'tags/series/index.atom',
        'tags/series/index.html',
        'tags/three/index.atom',
        'tags/three/index.html',
        'tags/two/index.atom',
        'tags/two/index.html',
    ]

    def test_generation(self):
        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
                output_dir=self.tempdir,
            )
            assert len(warnings) == 2

        with pytest.warns(None) as warnings:
            # one template has an invalid url() use
            flourish.generate_site()
            assert len(warnings) == 1
            assert 'tags-tag-page' in str(warnings[0].message)

        self.compare_directories()
