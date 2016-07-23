import pytest

from flourish import Flourish
from flourish.generators import (
    AtomGenerator,
    IndexGenerator,
    PageGenerator,
)

from .compare_directories import CompareDirectories


class TestFlourishGeneration(CompareDirectories):
    expected_directory = 'tests/output'
    expected_files = [
        'basic-page.html',
        'index.atom',
        'index.html',
        'markdown-page.html',
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
        class OnePageIndex(IndexGenerator):
            def get_objects(self, tokens):
                _objects = self.get_filtered_sources().filter(**tokens)[0:1]
                self.source_objects = _objects
                return _objects

        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
                output_dir=self.tempdir,
            )
            assert len(warnings) == 2

        flourish.add_url(
            '/#slug',
            'page-detail',
            PageGenerator.as_generator(),
        )
        flourish.add_url(
            '/',
            'homepage',
            IndexGenerator.as_generator(),
        )
        flourish.add_url(
            '/tags/#tag/',
            'tags-tag-page',
            OnePageIndex.as_generator(),
        )
        flourish.add_url(
            '/index.atom',
            'atom-feed',
            AtomGenerator.as_generator(),
        )
        flourish.add_url(
            '/tags/#tag/index.atom',
            'tags-atom-feed',
            AtomGenerator.as_generator(),
        )

        flourish.generate_all_urls()
        self.compare_directories()
