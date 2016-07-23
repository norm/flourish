from setuptools import find_packages, setup

# read in __version__
execfile('flourish/version.py')


setup(
    name='flourish',
    version=__version__,    # noqa: F821

    description='Static website generator',
    url='https://github.com/norm/flourish',

    license='MIT',
    author='Mark Norman Francis',
    author_email='norm@201created.com',

    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['flourish=flourish.command_line:main'],
    },

    install_requires=[
        'boto3',
        'Flask',
        'Jinja2',
        'markdown2',
        'pyatom',
        'toml',
        'watchdog',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
