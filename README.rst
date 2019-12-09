=========
CSV Tools
=========

CSV Tools is a *Processing* plugin for QGIS that adds algorithms to deal with
CSV files.

* Project repository and homepage: https://github.com/ygversil/qgis-plugin-csv-tools


What algorithms ?
=================

Currently, the following algorithms are provided:

* load a CSV file as a vector layer,

* export a vector layer as a CSV file,

* Compute difference between layers.

The last one works by converting both layers to CSV, and computing diff between
the two CSV files. Of course it does only make sense for layers with same
columns, so that the difference shows added, removed or modified lines.


What for ?
==========

These algorithms can become the building blocks of more complex workflows.

As an illustration you can use the Load CSV algorithm in the *graphical
modeler* to automatically, and moreover *quickly*, extract data from a large
Postgis table, given an extent for example. This is faster than loading the
table directly in QGIS with an SQL filter because it uses the PotgreSQL
``COPY`` command. And the resulting model shows an easier user interface (just
draw an extent, click run, and you get the data).


License
=======

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
