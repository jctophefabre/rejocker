###################################
rejocker is a REst Json mOCK servER
###################################


rejocker is a simple configurable mock server. It is mainly dedicated to the testing of REST clients.

* Support configuration of headers and bodies in resquests and responses
* Accept and respond with JSON and plain text
* Support GET,POST,PUT,PATCH and DELETE methods for HTTP requests
* Return HTTP status codes


Requirements
============

rejocker is written in `Python 3 <https://www.python.org/>`_ using the `Flask 1.1.x <https://flask.palletsprojects.com/>`_ framework, 
and is provided as a Python package

To install the package dependencies, you can run the following command from the root directory of the source code

.. code-block:: shell

  pip3 install -r requirements.txt


Usage
=====

Configuration
-------------

rejocker is configured through a json formatted file defining endpoints. 
Each endpoint is defined with 

* a path (and an optional path prefix)
* accepted HTTP methods 
* expected and returned headers and bodies for each method

Th location of the configuration file is given to rejocker through the ``REJOCKER_DATA_SOURCE`` environment variable.
(E.g. ``REJOCKER_DATA_SOURCE=/path/to/config.json``)

An example of a configuration file is provided with the rejocker package in the ``data`` directory. 
If the ``REJOCKER_DATA_SOURCE`` environment variable is not set, the example file is used by default.


Running the server locally
--------------------------

The server can be run locally for development or testing purposes.

First, the rejocker package have to be installed locally (this should be done oonly once):
 
.. code-block:: shell
 
  pip3 install -e .


To run the server:

.. code-block:: shell

  FLASK_APP=rejocker flask run

To run the server in development mode and automatic reload of source code:

.. code-block:: shell
  
  FLASK_ENV=development FLASK_APP=rejocker flask run --reload


You can visit the `Flask Quickstart <https://flask.palletsprojects.com/en/1.1.x/quickstart/>`_ for details.


Running the server in production
--------------------------------

In production, the server must be run according to the `Flask recommendations for deployment <https://flask.palletsprojects.com/en/1.1.x/deploying/>`_.
