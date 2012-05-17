from setuptools import find_packages
from setuptools import setup


setup(
    name='collective.searchevent',
    version=0.0,
    description="Search Event",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1"
        "Framework :: Plone :: 4.2"
        "Framework :: Plone :: 4.3"
        "Programming Language :: Python",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'five.grok',
        'hexagonit.testing',
        'plone.app.portlets',
        'plone.app.relationfield',
        'plone.browserlayer',
        'plone.formwidget.datetime',
        'setuptools',
        'zope.i18nmessageid',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
