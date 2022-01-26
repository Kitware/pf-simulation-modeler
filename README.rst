==========================
ParFlow Simulation Modeler
==========================

Simulation modeler for ParFlow

With this app a user can model various runs of the `ParFlow hydrologic simulator <https://www.parflow.org/>`_.


* Free software: BSD license


Development
----------
Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

Create a virtual environment to use with your `ParaView 5.10+ <https://www.paraview.org/download/>`_

.. code-block:: console

    python3.9 -m venv .venv
    source .venv/bin/activate
    python -m pip install -U pip
    pip install -e .

Run the application using `ParaView: pvpython <https://www.paraview.org/>`_ executable

.. code-block:: console

    export PV_VENV=$PWD/.venv
    /Applications/ParaView-5.10.0.app/Contents/bin/pvpython \ # Using macOS install path as example
        pv_run.py \
        -O ./data/output/little_washita \
        -D ./data/database \
        -S ./data/share \
        --server --dev


Run application
---------------

Create a virtual environment to use with your `ParaView 5.10.1+ <https://www.paraview.org/download/>`_

.. code-block:: console

    python3.9 -m venv .venv
    source .venv/bin/activate
    python -m pip install -U pip
    pip install pf-simulation-modeler

Run the application using `ParaView: pvpython <https://www.paraview.org/>`_ executable with environment variables:

.. code-block:: console

    export PV_VENV=$PWD/.venv
    export TRAME_APP=pf_modeler
    pvpython -m paraview.apps.trame \
        -O ./data/output/little_washita \
        -D ./data/database \
        -S ./data/share


Or with command line arguments:

.. code-block:: console

    pvpython -m paraview.apps.trame \
        --venv $PWD/.venv \
        --trame-app pf_modeler \
        -O ./data/output/little_washita \
        -D ./data/database \
        -S ./data/share