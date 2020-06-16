import argparse
from hashlib import md5
import os
import textwrap

import boto3
from flask import Flask, send_from_directory

from . import Flourish, __version__
from .examples import example_files
from .lib import relative_list_of_files_in_directory


def main():
    version = ('Flourish static site generator, version %s -- '
               'http://withaflourish.net' % __version__)
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            Flourish generates websites from source data and templates.
            Version %s -- http://withaflourish.net

            Commands:
                generate        creates the output HTML
                preview         preview the generated content from your local
                                computer before uploading
                example         creates a new flourish website in the
                                current directory, with some example content
                upload          upload the generated site to an AWS S3 bucket
        """ % __version__),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'action', nargs='?', choices=ACTIONS.keys()),
    parser.add_argument(
        '-b', '--base', default=None,
        help='Base directory that contains all others')
    parser.add_argument(
        '-s', '--source', default='source',
        help='Directory containing source files (default: %(default)s)')
    parser.add_argument(
        '-t', '--templates', default='templates',
        help='Directory containing templates (default: %(default)s)')
    parser.add_argument(
        '-o', '--output', default='output',
        help='Directory to output to (default: %(default)s)')
    parser.add_argument(
        '-p', '--port', default='3567',
        help='Port on which to bind preview webserver (default: %(default)s)')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Report each URL as it is generated')
    parser.add_argument(
        '--version', action='store_true',
        help='Report the version of flourish')
    parser.add_argument(
        '--rebuild', action='store_true',
        help=(
            'When previewing a site, '
            'regenerate the requested page before serving'
        ))
    parser.add_argument(
        '--bucket',
        help='The name of the AWS S3 bucket to upload to (with upload)')

    args = parser.parse_args()

    if args.version:
        print(version)
    elif args.action is None:
        parser.print_help()
    else:
        if args.base is not None:
            args.source = os.path.join(args.base, args.source)
            args.templates = os.path.join(args.base, args.templates)
            args.output = os.path.join(args.base, args.output)
        action = ACTIONS[args.action]
        action(args)


def generate(args):
    flourish = Flourish(
        source_dir=args.source,
        templates_dir=args.templates,
        output_dir=args.output,
    )
    flourish.generate_site(report=args.verbose)


def preview_server(args):
    output_dir = os.path.abspath(args.output)
    app = Flask(__name__)

    # TODO 3xx redirects
    # TODO 404 page
    # TODO 410 page
    @app.route('/')
    @app.route('/<path:path>')
    def send_file(path=''):
        generate = '/%s' % path

        # fix URLs for .html
        filename = os.path.basename(path)
        if filename == '':
            path = '%sindex.html' % path
        _, ext = os.path.splitext(path)
        if ext == '':
            path += '.html'

        # regenerate if requested
        if args.rebuild:
            flourish = Flourish(
                source_dir=args.source,
                templates_dir=args.templates,
                output_dir=args.output,
            )
            flourish.generate_path(generate, report=args.verbose)

        print('<-', path)
        return send_from_directory(output_dir, path)

    @app.after_request
    def add_header(response):
        response.cache_control.max_age = 0
        return response

    app.run(port=args.port)


def create_example(args):
    for _dir in ['source', 'templates']:
        if not os.path.isdir(_dir):
            os.mkdir(_dir)
    for _filename in example_files:
        with open(_filename, 'w') as _example_file:
            _example_file.write(example_files[_filename])
    generate(argparse.Namespace(
        source='source',
        templates='templates',
        output='output',
    ))
    print('Example site created: run "flourish --rebuild preview"')
    print('and go to http://localhost:3567/ in your browser to see the site.')
    print('Then click on "Welcome to your new blog" to get started.')


def upload(args):
    _bucket_name = args.bucket
    if _bucket_name is None:
        flourish = Flourish(args.source, args.templates, args.output)
        _bucket_name = flourish.site_config['bucket']

    # FIXME remove nonexistent files
    _s3 = boto3.resource('s3')
    _bucket = _s3.Bucket(_bucket_name)
    _files = relative_list_of_files_in_directory(args.output)
    _objects = dict()
    for _object in _bucket.objects.all():
        _objects.update({_object.key: _object})

    for _path in _files:
        _type = None
        _file = os.path.basename(_path)
        _s3path = _path
        if _file.endswith('.html'):
            _type = 'text/html'
            if not _file == 'index.html':
                _s3path = _path[:-5]

        _upload = True
        _md5 = '"%s"' % md5(
                open('%s/%s' % (args.output, _path), 'rb').read()
            ).hexdigest()
        try:
            if _md5 == _objects[_s3path].e_tag:
                _upload = False
        except KeyError:
            pass

        if _upload:
            print('->', _s3path)
            _object_args = {
                'Key': _s3path,
                'ACL': 'public-read',
                'Body': open('%s/%s' % (args.output, _path), 'rb'),
            }
            if _type:
                _object_args['ContentType'] = _type
            _bucket.put_object(**_object_args)


ACTIONS = {
    'generate': generate,
    'preview': preview_server,
    'example': create_example,
    'upload': upload,
}

if __name__ == '__main__':
    main()
