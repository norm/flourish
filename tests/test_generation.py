import pytest

from flourish import Flourish
from flourish.generators import IndexGenerator, PageGenerator

from .compare_directories import CompareDirectories


class TestFlourishGeneration(CompareDirectories):
    expected_directory = 'tests/output'
    expected_files = [
        'basic-page.html',
        'index.html',
        'markdown-page.html',
        'thing-one.html',
        'thing-two.html',
        'series/part-one.html',
        'series/part-three.html',
        'series/part-two.html',
        'tags/basic-page.html',
        'tags/basically.html',
        'tags/first.html',
        'tags/one.html',
        'tags/second.html',
        'tags/series.html',
        'tags/three.html',
        'tags/two.html',
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
            '/tags/#tag',
            'tags-tag-page',
            OnePageIndex.as_generator(),
        )

        flourish.generate_all_urls()
        self.compare_directories()
