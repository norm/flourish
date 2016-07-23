import argparse
from hashlib import md5
from imp import load_source
from multiprocessing import Process
import os
from shutil import rmtree
import sys
import textwrap
import time

import boto3
from flask import Flask, send_from_directory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
        '-a', '--assets', default='assets',
        help='Directory containing asset files (default: %(default)s)')
    parser.add_argument(
        '-o', '--output', default='output',
        help='Directory to output to (default: %(default)s)')
    parser.add_argument(
        '-p', '--port', default='3567',
        help='Port on which to bind preview webserver (default: %(default)s)')
    parser.add_argument(
        '-v', '--version', action='store_true',
        help='Report the version of flourish')
    parser.add_argument(
        '--rebuild', action='store_true',
        help='Watch the source and template directories for changes, '
             'regenerating the site automatically.')
    parser.add_argument(
        '--bucket',
        help='The name of the AWS S3 bucket to upload to (with upload)')

    args = parser.parse_args()

    if args.version:
        print version
    elif args.action is None:
        parser.print_help()
    else:
        if args.base is not None:
            args.source = os.path.join(args.base, args.source)
            args.templates = os.path.join(args.base, args.templates)
            args.assets = os.path.join(args.base, args.assets)
            args.output = os.path.join(args.base, args.output)
        action = ACTIONS[args.action]
        action(args)


def generate(args):
    if args.rebuild:
        generate_once(args)
        generate_on_change(args)
    else:
        generate_once(args)


def generate_once(args):
    generate = load_source('generate', '%s/generate.py' % args.source)

    if os.path.exists(args.output):
        rmtree(args.output)
    os.makedirs(args.output)

    flourish = Flourish(
        source_dir=args.source,
        templates_dir=args.templates,
        output_dir=args.output,
        assets_dir=args.assets,
    )

    try:
        flourish.set_global_context(getattr(generate, 'GLOBAL_CONTEXT'))
    except AttributeError:
        # global context is optional
        pass

    has_urls = False
    try:
        flourish.canonical_source_url(*generate.SOURCE_URL)
        has_urls = True
    except AttributeError:
        # source URLs are optional
        pass

    try:
        for url in generate.URLS:
            has_urls = True
            flourish.add_url(*url)
    except:
        # other URLs are optional
        pass

    if has_urls:
        flourish.generate_all_urls()
        flourish.copy_assets()
    else:
        # both types of URL are optional, but having one or the other is not
        print "Nothing to generate!"
        sys.exit(1)


def generate_on_change(args):
    class Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            print '**', event.src_path, event.event_type
            generate_once(args)

    generate_once(args)
    observer = Observer()
    observer.daemon = True
    observer.schedule(Handler(), args.source, recursive=True)
    observer.schedule(Handler(), args.templates, recursive=True)
    if os.path.exists(args.assets):
        # having assets is optional
        observer.schedule(Handler(), args.assets, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def preview_server(args):
    if args.rebuild:
        preview_rebuildserver(args)
    else:
        preview_runserver(args)


def preview_runserver(args):
    output_dir = os.path.abspath(args.output)
    app = Flask(__name__)

    # TODO 3xx redirects
    # TODO 404 page
    # TODO 410 page
    @app.route('/')
    @app.route('/<path:path>')
    def send_file(path=''):
        filename = os.path.basename(path)
        if filename == '':
            path = '%sindex.html' % path
        root, ext = os.path.splitext(path)
        if ext == '':
            path = '%s.html' % path
        print '->', path
        return send_from_directory(output_dir, path)

    @app.after_request
    def add_header(response):
        response.cache_control.max_age = 0
        return response

    app.run(port=3567)


def preview_rebuildserver(args):
    _server = Process(target=preview_runserver, args=(args,))
    _server.start()
    _goc = Process(target=generate_on_change, args=(args,))
    _goc.start()


def create_example(args):
    for _dir in ['source', 'templates', 'assets']:
        if not os.path.isdir(_dir):
            os.mkdir(_dir)
    for _filename in example_files:
        with open(_filename, 'w') as _example_file:
            _example_file.write(example_files[_filename])
    generate_once(argparse.Namespace(
        source='source',
        templates='templates',
        assets='assets',
        output='output',
    ))
    print 'Example site created: run "flourish --rebuild preview"'
    print 'and go to http://localhost:3567/ in your browser to see the site.'
    print 'Then click on "Welcome to your new blog" to get started.'


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
            print '->', _s3path
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
