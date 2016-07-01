import pytest

from flourish import Flourish
from flourish.generators import (
    AtomGenerator,
    IndexGenerator,
    PageGenerator,
    PaginatedIndexGenerator,
)

from .compare_directories import CompareDirectories


class TestFlourishGeneration(CompareDirectories):
    expected_directory = 'tests/output'
    expected_files = [
        'all/index.html',
        'all/page-2.html',
        'basic-page.html',
        'css/screen.css',
        'index.atom',
        'index.html',
        'logo.png',
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
        # FIXME move this all into tests/source/generate.py,
        # and call command_line generate
        class NewestFirstIndex(IndexGenerator):
            order_by = ('-published')

        class OnePageIndex(IndexGenerator):
            def get_objects(self, tokens):
                _objects = self.get_filtered_sources().filter(**tokens)[0:1]
                self.source_objects = _objects
                return _objects

        class FourPagePaginatedIndex(PaginatedIndexGenerator):
            order_by = ('published')
            per_page = 4


        with pytest.warns(None) as warnings:
            flourish = Flourish(
                source_dir='tests/source',
                templates_dir='tests/templates',
                assets_dir='tests/assets',
                output_dir=self.tempdir,
            )
            assert len(warnings) == 2

        flourish.canonical_source_url(
            '/#slug',
            PageGenerator.as_generator(),
        )
        flourish.add_url(
            '/',
            'homepage',
            NewestFirstIndex.as_generator(),
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
        flourish.add_url(
            '/all/',
            'all-paginated',
            FourPagePaginatedIndex.as_generator(),
        )

        flourish.generate_all_urls()
        flourish.copy_assets()
        self.compare_directories()
