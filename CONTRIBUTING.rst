===================
How to contribute ?
===================

Writing code
============

Writing code is one obvious way to help us. For example, you can either fix a
bug or develop a new functionality. To do so, you must have a Framagit_
account (powered by GitLab_).

Preliminary steps
-----------------

First you need to clone the source code repository, both on your Framagit
account (this is called a *fork*) and locally on your computer. Then, before
doing anything else, make sure that everything is working fine.

Follow the following instructions if your operating system is a GNU/Linux
distribution.  You must have previously installed git, Python 3, and of course
QGIS 3.X.

* Web browse to the project repository on Framagit interface:
  https://framagit.org/ygversil/qgis-processing-csv-tools/. Then click on the
  ``Fork`` button to clone the repository into your own account.

* On your computer, clone your forked repository in a suitable folder::

    $ cd <path/to/your/source/folder>
    $ git clone git@framagit.org:<your_framagit_username>/qgis-processing-csv-tools/

  Of course, replace ``<path/to/your/source/folder>`` with the path to a folder
  where you keep source code, and ``<your_framagit_username>`` with your
  Framagit username (you should have set up SSH *key-based authentication*
  previously for this to work flawlessly. See https://docs.gitlab.com/ee/ssh/
  for details).

* In the project folder, create a Python virtual environment (venv) for the
  project::

    $ cd qgis-processing-csv-tools
    $ python -m venv venv

* This will create a ``venv`` folder. You can now activate the venv::

    $ source venv/bin/activate

  (Later, to disable the venv you can simply run ``deactivate``).

* Install needed dependencies inside the venv::

    (venv)$ pip install -r requirements.txt

* Make sure QGIS librairies can be found by the plugin. Source the script
  ``scripts/run-env-linux.sh`` giving as a parameter the folder containing the
  QGIS ``lib`` folder. For example, if you have installed QGIS using a system
  binary package manager (``apt-get``, ``yum`` or the like), the QGIS ``lib``
  folder is at ``/usr/lib`` path, so run::

    (venv)$ source scripts/run-env-linux.sh /usr

  If however you have installed QGIS in ``/opt/qgis-3.0``, then the ``lib``
  folder is at ``/opt/qgis-3.0/lib``, so the command is::

    (venv)$ source scripts/run-env-linux.sh /opt/qgis-3.0

  You are advised to source the script each time you activate the venv. Simply
  copy and paste the following line at the end of the ``venv/bin/activate``
  file, replacing the path with the correct one::

    source <path/to/your/source/folder>/qgis-processing-csv-tools/scripts/run-env-linux.sh </path/to/folder/containing/QGIS/lib>

* Find the path to the ``plugins`` folder where you will test your changes. You
  are advised to use a specific QGIS profile for development purposes. Keep it
  separate from the default profile. The path may looks like::

    /home/<username>/.local/share/QGIS/QGIS3/profiles/dev/python/plugins/

  Then create the file ``pb_tool.cfg`` copying the provided template
  ``pb_tool.cfg.tmpl`` and replace the line starting with ``plugin_path:`` with
  the aforementioned path.

* Finally, make sure that tests are passing::

    (venv)$ make test

.. _Framagit: https://framagit.org/

.. _GitLab: https://about.gitlab.com/
