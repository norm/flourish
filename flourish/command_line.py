import argparse
from datetime import datetime
from hashlib import md5
import mimetypes
import os
import sys
from textwrap import dedent
import time

import boto3
from flask import Flask, make_response, redirect, request, send_from_directory
from jinja2 import Template
from sectile import Sectile

from . import Flourish, __version__, blueprint
from .examples import example_files
from .lib import relative_list_of_files_in_directory

REDIRECT_ETAG='"d41d8cd98f00b204e9800998ecf8427e"'      # 0 byte file


def main():
    version = ('Flourish static site generator, version %s -- '
               'http://withaflourish.net' % __version__)
    parser = argparse.ArgumentParser(
        description=(
            'Flourish generates websites from source data and templates.'
        ),
        epilog=(
            'Version %s -- http://withaflourish.net' % __version__
        ),
    )
    parser.add_argument(
        '--base',
        default=None,
        help='Base directory that contains all others (default: .)',
    )
    parser.add_argument(
        '--source',
        default='source',
        help='Directory containing source files (default: %(default)s)',
    )
    parser.add_argument(
        '--templates',
        default='templates',
        help='Directory containing templates (default: %(default)s)',
    )
    parser.add_argument(
        '--fragments',
        default='fragments',
        help=(
            'Directory containing Sectile template fragments'
            ' (experimental feature, no default)'
        ),
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Directory to output to (default: %(default)s)',
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Report the version of flourish',
    )
    subparsers = parser.add_subparsers(
        title='Actions',
        description=(
            'To get more information, run "flourish [command] --help".'
        ),
        dest='action',
    )

    parser_generate = subparsers.add_parser(
        'generate',
        help='creates the output HTML',
    )
    parser_generate.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Report each URL as it is generated'
    )
    parser_generate.add_argument(
        '--include-future',
        action='store_true',
        help=(
            'Include sources with a publication date in the future, '
            'overriding the "future" setting in _site.toml.'
        ),
    )
    parser_generate.add_argument(
        '--exclude-future',
        action='store_true',
        help=(
            'Exclude sources with a publication date in the future, '
            'overriding the "future" setting in _site.toml.'
        ),
    )
    parser_generate.add_argument(
        'path',
        nargs='*',
        help=(
            'Generate only this path (appending ? makes it a wildcard '
            'match to generate anything that starts with this path '
            ' -- eg. /2020/?). Can be specified repeatedly.'
        ),
    )

    parser_preview = subparsers.add_parser(
        'preview',
        help=(
            'preview the generated content from your local computer '
            'before uploading'
        ),
    )
    parser_preview.add_argument(
        '-p', '--port',
        default='3567',
        help='Port on which to bind preview webserver (default: %(default)s)',
    )
    parser_preview.add_argument(
        '-g', '--generate',
        action='store_true',
        help='Regenerate the requested page before serving',
    )

    parser_upload = subparsers.add_parser(
        'upload',
        help='upload the generated site to an AWS S3 bucket',
    )
    parser_upload.add_argument(
        '--dry-run',
        action='store_true',
        help='only list what would be uploaded',
    )
    parser_upload.add_argument(
        '--invalidate',
        action='store_true',
        help='invalidate uploaded paths in CloudFront',
    )
    parser_upload.add_argument(
        'bucket',
        nargs='?',
        help='bucket to upload to (default: bucket entry in _site.toml)',
    )
    parser_upload.add_argument(
        'cloudfront_id',
        nargs='?',
        help='the CloudFront distribution ID',
    )

    parser_example = subparsers.add_parser(             # noqa: F841
        'example',
        help=(
            'creates a new flourish website in the '
            'current directory with some example content'
        ),
    )

    args = parser.parse_args()
    if args.version:
        print(version)
    elif args.action is None:
        parser.print_help()
    else:
        if args.base is not None:
            args.source = os.path.join(args.base, args.source)
            args.templates = os.path.join(args.base, args.templates)
            args.fragments = os.path.join(args.base, args.fragments)
            args.output = os.path.join(args.base, args.output)
        # find default 'fragments' directory but without forcing it
        if not os.path.isdir(args.fragments):
            args.fragments = None
        action = ACTIONS[args.action]
        action(args)


def generate(args):
    future = None
    if args.exclude_future:
        future = False
    if args.include_future:
        future = True
    try:
        flourish = Flourish(
            source_dir=args.source,
            templates_dir=args.templates,
            fragments_dir=args.fragments,
            output_dir=args.output,
            future=future,
        )
    except Flourish.MissingKey as e:
        sys.exit('Error: %s' % str(e))
    except Flourish.RuntimeError as e:
        sys.exit('Error: %s' % str(e))
    if args.path:
        for path in args.path:
            flourish.generate_path(path, report=args.verbose)
    else:
        flourish.generate_site(report=args.verbose)


def preview_server(args):
    output_dir = os.path.abspath(args.output)
    source_dir = os.path.abspath(args.source)
    reloading = False
    if args.generate:
        reloading = True
    try:
        flourish = Flourish(
            source_dir=args.source,
            templates_dir=args.templates,
            fragments_dir=args.fragments,
            output_dir=args.output,
            reloading=reloading,
        )
    except Flourish.MissingKey as e:
        sys.exit('Error: %s' % str(e))
    except Flourish.RuntimeError as e:
        sys.exit('Error: %s' % str(e))
    app = Flask(__name__)

    # TODO 3xx redirects
    # TODO 404 page
    # TODO 410 page
    @app.route('/')
    @app.route('/<path:path>')
    def send_file(path=''):
        generate = '/%s' % path

        if generate in flourish.redirects:
            return redirect(flourish.redirects[generate])

        if 'blueprint' in request.args:
            response = make_response(
                Template(
                    blueprint.template
                ).render(
                    flourish.path_blueprint(generate)
                )
            )
            response.headers.set('X-Blueprint-Page', 'true')
            return response
        else:
            # fix URLs for .html
            filename = os.path.basename(path)
            if filename == '':
                path = '%sindex.html' % path
            _, ext = os.path.splitext(path)
            if ext == '':
                path += '.html'

            # regenerate if requested
            if args.generate:
                try:
                    os.remove(os.path.join(output_dir, path))
                except FileNotFoundError:
                    pass
                flourish.generate_path(generate, report=True)

            if os.path.exists(os.path.join(output_dir, path)):
                return send_from_directory(output_dir, path)
            else:
                return send_from_directory(source_dir, path)

    @app.route('/_sectile/update', methods=['GET', 'POST'])
    def edit_sectile_fragment():
        sectile = Sectile(fragments=args.fragments)
        if request.method == 'GET':
            return make_response(
                    Template(
                        blueprint.update_template
                    ).render({
                        'fragment': request.args['fragment'],
                        'content': sectile.get_fragment_file(request.args['fragment']),
                        '_return': request.args['_return'],
                    })
                )
        else:
            sectile.update_fragment(
                request.form['fragment'],
                request.form['content'],
            )
            return redirect(request.form['_return'])

    @app.route('/_sectile/delete', methods=['POST'])
    def delete_sectile_fragment():
        sectile = Sectile(fragments=args.fragments)
        sectile.delete_fragment(request.form['fragment'])
        return redirect(request.form['_return'])

    @app.route('/_sectile/create', methods=['POST'])
    def create_sectile_fragment():
        sectile = Sectile(fragments=args.fragments)
        dimensions = {}
        for dimension in sectile.get_dimensions_list():
            dimensions[dimension] = request.form[dimension]
        sectile.create_fragment(
            request.form['fragment'],
            request.form['path'],
            **dimensions,
        )
        return redirect(request.form['_return'])

    @app.after_request
    def add_header(response):
        if (
            response.content_type.startswith('text/html')
            and args.generate
            and not 'X-Blueprint-Page' in response.headers
        ):
            response.direct_passthrough = False
            response.data = (
                response.data + bytes(blueprint.toolbar, 'utf-8')
            )
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
        action='generate',
        verbose=True,
        path=[],
    ))
    print('Example site created: run "flourish preview --generate"')
    print('and go to http://localhost:3567/ in your browser to see the site.')
    print('Then click on "Welcome to your new blog" to get started.')


def upload(args):
    mimetypes.init()

    try:
        flourish = Flourish(
            source_dir=args.source,
            templates_dir=args.templates,
            fragments_dir=args.fragments,
            output_dir=args.output,
        )
    except Flourish.MissingKey as e:
        sys.exit('Error: %s' % str(e))
    except Flourish.RuntimeError as e:
        sys.exit('Error: %s' % str(e))

    _bucket_name = args.bucket
    _cloudfront = args.cloudfront_id
    if _bucket_name is None:
        _bucket_name = flourish.site_config['bucket']
    if args.invalidate and args.cloudfront_id is None:
        _cloudfront = flourish.site_config['cloudfront_id']

    # FIXME remove nonexistent files
    _s3 = boto3.resource('s3')
    _bucket = _s3.Bucket(_bucket_name)
    _files = relative_list_of_files_in_directory(args.output)
    _objects = dict()
    _invalidations = []
    for _object in _bucket.objects.all():
        _objects.update({_object.key: _object})

    redirects = flourish.redirects
    for redirect in redirects:
        _s3path = redirect[1:]
        if (
            _s3path not in _objects
            or _objects[_s3path].e_tag != REDIRECT_ETAG
        ):
            print('->', redirect, 'to', redirects[redirect])
            if not args.dry_run:
                _bucket.put_object(
                    Key=_s3path,
                    Body='',
                    ContentType='text/html',
                    WebsiteRedirectLocation=redirects[redirect],
                )
                _invalidations.append(redirect)

    for _path in _files:
        _file = os.path.basename(_path)
        _type, _ = mimetypes.guess_type(_file)
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
            print('>>', _s3path)
            if not args.dry_run:
                _object_args = {
                    'Key': _s3path,
                    'ACL': 'public-read',
                    'Body': open('%s/%s' % (args.output, _path), 'rb'),
                    'ContentType': _type,
                }
                _bucket.put_object(**_object_args)
                invalidate = '/' + _s3path
                if invalidate.endswith('index.html'):
                    invalidate = invalidate[:-10]
                _invalidations.append(invalidate)

    if args.invalidate and _invalidations:
        cf = boto3.client('cloudfront')
        result = cf.create_invalidation(
            DistributionId=_cloudfront,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(_invalidations),
                    'Items': _invalidations,
                },
                'CallerReference': datetime.now().isoformat(),
            }
        )
        invalidation_id = result['Invalidation']['Id']
        print('Invalidating distribution %s: %s' % (_cloudfront, invalidation_id))
        while True:
            time.sleep(15)
            status = cf.get_invalidation(
                DistributionId = _cloudfront,
                Id = invalidation_id,
            )
            print(
                datetime.now().strftime('%H:%M:%S'),
                invalidation_id,
                status['Invalidation']['Status'],
            )
            if status['Invalidation']['Status'] == 'Completed':
                break

ACTIONS = {
    'generate': generate,
    'preview': preview_server,
    'example': create_example,
    'upload': upload,
}

if __name__ == '__main__':
    main()
