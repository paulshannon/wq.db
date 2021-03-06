import os
import sys
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Django design patterns and REST API for field data collection.
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


def create_wq_namespace():
    """
    Generate the wq namespace package
    (not checked in, as it technically is the parent of this folder)
    """
    if os.path.isdir("wq"):
        return
    os.makedirs("wq")
    init = open(os.path.join("wq", "__init__.py"), 'w')
    init.write("__import__('pkg_resources').declare_namespace(__name__)")
    init.close()


def create_wqdb_namespace():
    """
    Since tests aren't picking up package_dir, populate wq.db namespace with
    symlinks back to top level directories.
    """
    if os.path.isdir("wq/db"):
        return
    os.makedirs("wq/db")
    for folder in ("rest", "contrib", "patterns", "default_settings.py"):
        os.symlink("../../" + folder, "wq/db/" + folder)
    init = open(os.path.join("wq/db", "__init__.py"), 'w')
    init.write("")
    init.close()


def find_wq_packages(submodule):
    """
    Add submodule prefix to found packages, since the packages within each wq
    submodule exist at the top level of their respective repositories.
    """
    packages = ['wq', submodule]
    package_dir = {submodule: '.'}
    for package in find_packages():
        if package.split('.')[0] in ('wq', 'tests'):
            continue
        full_name = submodule + "." + package
        packages.append(full_name)
        package_dir[full_name] = package.replace('.', os.sep)

    return packages, package_dir


create_wq_namespace()
packages, package_dir = find_wq_packages('wq.db')

if len(sys.argv) > 1 and sys.argv[1] == "test":
    create_wqdb_namespace()

setup(
    name='wq.db',
    version='0.8.2-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://wq.io/wq.db',
    license='MIT',
    packages=packages,
    package_dir=package_dir,
    namespace_packages=['wq'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=[
        'Django>=1.7',
        'djangorestframework>=3.1',
        'pystache',
        'swapper>=0.2',
        'Markdown',
    ],
    extras_require={
        'chart': ['rest_pandas>=0.3.1'],
        'files': ['wq.io>=0.5.1', 'Pillow'],
        'social': ['python-social-auth'],
    },
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Database :: Database Engines/Servers',
    ],
    test_suite='tests',
    tests_require=[
        'psycopg2',
        'wq.io>=0.5.1',
        'rest_pandas>=0.3.1',
        'Pillow',
        'python-social-auth==0.2.7',
    ],
)
