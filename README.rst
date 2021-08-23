.. image:: https://github.com/dataPuzzler/dp_sqlalchemy_wrapper/actions/workflows/test.yml/badge.svg?branch=master&event=workflow_dispatch
	:target: https://github.com/dataPuzzler/dp_sqlalchemy_wrapper/actions/workflows/test.yml/badge.svg?branch=master&event=workflow_dispatch
	:alt: Unit-tests Badge

dp_sqlalchemy_wrapper
=====================

*dp_sqlalchemy_wrapper* is a slim wrapper around sqlalchemy to accelerate database setup and to ease common database operations.

Installing
----------

Install and update using `pip`:

.. code-block:: text

    # Default Installation 
    pip install dp_sqlalchemy_wrapper
    
    # With facility to populate tables from json data
    pip install dp_sqlalchemy_wrapper[json_fill] 
