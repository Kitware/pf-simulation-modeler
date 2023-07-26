# {project_name}

Firstly, make sure you have ParFlow built and installed.

- [Ubuntu Install Guide](https://github.com/parflow/parflow/wiki/Ubuntu-20.04.1-LTS---Factory-condition)
- [General install info](https://github.com/parflow/parflow/wiki/ParFlow-Installation-Guides)

## Python Setup

Following the ParFlow guide for getting started in python with `pftools`: [Getting Started](https://parflow.readthedocs.io/en/latest/python/getting_started.html)

### Making a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install pftools[all]
```

Make sure you have all of `pftools` installed. Occasionally you may need to specify an older version of `numpy` to get all the modules to install.

### Execute the program

Once you have all the packages installed, you can run the program.

```bash
python {project_name}.py
```

See [pftools docs](https://parflow.readthedocs.io/en/latest/python/getting_started.html) for more information.
