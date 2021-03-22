from datetime import datetime, timezone
import os

from feedgen.feed import FeedGenerator

from flourish.generators.base import BaseGenerator
from flourish.generators.mixins import SourcesMixin


class AtomGenerator(SourcesMixin, BaseGenerator):
    order_by = ('-published')
    file_extension = '.atom'
    limit = 20
    required_config_keys = ('author', 'base_url', 'title')

    def get_objects(self, tokens):
        """
        Only consider objects that have the key "published" with a
        datetime value that is in the past.
        """
        _now = datetime.now().replace(tzinfo=timezone.utc)
        _sources = self.get_filtered_sources()
        _already_published = _sources.filter(published__lt=_now)
        _filtered = _already_published.filter(**tokens)
        _ordered = _filtered.order_by(self.order_by)

        if self.limit is not None:
            self.source_objects = _ordered[0:self.limit]
        else:
            self.source_objects = _ordered

        return self.source_objects

    def render_output(self):
        feed = FeedGenerator()
        feed.author({'name': self.flourish.site_config['author']})
        feed.title(self.flourish.site_config['title'])
        # feed.link(self.flourish.site_config['base_url'])
        feed.id('%s%s' % (
            self.flourish.site_config['base_url'],
            self.current_path,
        ))
        feed.link(href='%s%s' % (
                self.flourish.site_config['base_url'],
                self.current_path,
            ), rel='self')
        feed.link(href=self.flourish.site_config['base_url'], rel='alternate')

        last_updated = self.source_objects[0].published

        for _object in self.source_objects:
            entry = feed.add_entry(order='append')
            entry.title(self.get_entry_title(_object))
            entry.id(self.get_entry_id(_object))
            entry.link(href=_object.absolute_url, rel='alternate')
            entry.published(_object.published)
            entry.content(
                content=self.get_entry_content(_object),
                type='html'
            )

            if 'author' in _object:
                entry.author({'name': _object.author})
            else:
                entry.author({'name': self.flourish.site_config['author']})

            if 'updated' in _object:
                entry.updated(_object.updated)
                if _object.updated > last_updated:
                    last_updated = _object.updated
            else:
                entry.updated(_object.published)

        feed.updated(last_updated)

        return feed.atom_str(pretty=True)

    def get_entry_content(self, object):
        return object.body

    def get_entry_title(self, object):
        return object.title

    def get_entry_id(self, object):
        return object.absolute_url

    # FIXME refactor
    def output_to_file(self):
        _filename = self.get_output_filename()
        if self.report:
            print('->', _filename)

        _rendered = self.render_output()
        _directory = os.path.dirname(_filename)
        if not os.path.isdir(_directory):
            os.makedirs(_directory)
        with open(_filename, 'wb') as _output:
            _output.write(_rendered)
