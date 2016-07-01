import argparse
from imp import load_source
from multiprocessing import Process
import os
from shutil import rmtree
import textwrap
import time

from flask import Flask, send_from_directory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from . import Flourish


def main():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            Flourish generates websites from source and templates.

            Commands:
                generate        creates the output HTML
                server          serves up output HTML on a local port, good for
                                development previewing of work
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'action', choices=ACTIONS.keys()),
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
        help='Port on which to bind webserver (default: %(default)s)')
    parser.add_argument(
        '--rebuild', action='store_true',
        help='Watch the source and template directories for changes, '
             'regenerating the site automatically.')

    args = parser.parse_args()
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

    rmtree(args.output)

    flourish = Flourish(
        source_dir=args.source,
        templates_dir=args.templates,
        output_dir=args.output,
        assets_dir=args.assets,
    )

    flourish.canonical_source_url(*generate.SOURCE_URL)
    for url in generate.URLS:
        flourish.add_url(*url)
    flourish.generate_all_urls()
    flourish.copy_assets()


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
    observer.schedule(Handler(), args.assets, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def server(args):
    if args.rebuild:
        rebuildserver(args)
    else:
        runserver(args)


def runserver(args):
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


def rebuildserver(args):
    _server = Process(target=runserver, args=(args,))
    _server.start()
    _goc = Process(target=generate_on_change, args=(args,))
    _goc.start()


ACTIONS = {
    'generate': generate,
    'server': server,
}

if __name__ == '__main__':
    main()
