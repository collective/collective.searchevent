======================
collective.searchevent
======================

collective.searchevent provides **Search Event Portlet** for searching Plone default Event content type.

It is also possible to filter the search with tags (Subjects) and paths.

Filtering
---------

To make filtering work, you need to go to **Search Event Collections** from **Site Setup**: **Add-on Configuration** section and add **Event Search Collection** which will then be selected in the search event portlet management page.

Exporting
---------

Exporting search event results to csv file is available for roles who have Modify Portal Content permission who can see **Export** button on the portlet.
The separation of each values are done by '``|``'.

Currently tested with
---------------------

* Plone-4.2.3
