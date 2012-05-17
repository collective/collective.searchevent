Installation
============

Use zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``collective.searchevent`` to the list of eggs to install like::

    [buildout]
    ...
    eggs =
        ...
        collective.searchevent

* Re-run buildout, e.g. with::

    $ ./bin/buildout
