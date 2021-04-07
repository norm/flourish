import csv
from datetime import datetime

from flourish.generators.base import BaseGenerator
from flourish.generators.mixins import SourcesMixin


class CSVGenerator(SourcesMixin, BaseGenerator):
    file_extension = '.csv'
    fields = ['title', 'published']

    def output_to_file(self):
        filename = self.get_output_filename()
        with open(filename, 'w', newline='') as handle:
            output = csv.DictWriter(
                handle,
                fieldnames = self.get_fields(),
                quoting=csv.QUOTE_MINIMAL,
            )
            output.writeheader()

            for object in self.source_objects:
                output.writerow(self.get_row(object))

    def get_fields(self):
        return self.fields

    def get_row(self, object):
        row = {}
        for field in self.get_fields():
            row.update({field: self.get_field_value(object, field)})
        return row

    def get_field_value(self, object, field):
        value = getattr(object, field, None)
        if type(value) == list:
            if type(value[0]) == str:
                return ':'.join(sorted(value))
        elif type(value) == datetime:
            return value.isoformat().replace('+00:00', 'Z')
        return value
