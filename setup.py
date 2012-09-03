from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('collective', 'searchevent', 'docs', 'README.rst') + "\n" +
    read('collective', 'searchevent', 'docs', 'HISTORY.rst') + "\n" +
    read('collective', 'searchevent', 'docs', 'CONTRIBUTORS.rst') + "\n" +
    read('collective', 'searchevent', 'docs', 'CREDITS.rst'))


setup(
    name='collective.searchevent',
    version='0.3',
    description="Adds portlet to search event content types for Plone.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/collective/collective.searchevent',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone>=4.2',
        'five.grok',
        'hexagonit.testing',
        'plone.app.contentlisting',
        'plone.app.portlets',
        'plone.app.relationfield',
        'plone.behavior',
        'plone.browserlayer',
        'plone.directives.form',
        'plone.formwidget.datetime',
        'setuptools',
        'zope.i18nmessageid'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
