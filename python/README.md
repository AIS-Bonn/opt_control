# Python Interface to opt_control

This Python package provides an interface to the underlying opt_control C++ library.

# Install the package.

These command line examples assume your working directory is already ```opt_control/python``` and you are already in a Python 3 virtual environment.

* First build the shared library.

```
$ make
```

* Then install the Python package in editable mode from local source.

```
$ pip install -e .
```

# Test your installation.

```
$ python tests/eval_example.py
```

# Tips

It is always advisable to do Python development in a vitual environment. If this is an unfamiliar topic, here is a generic example/recommendation.

* One time, create a virtual environment called 'opt' somewhere convenient.

```
python3 -m venv ~/venv/opt
source ~/venv/opt/bin/activate
pip install --upgrade pip
```

* In the future, access your 'opt' virtual environment again with

```
source ~/venv/opt/bin/activate
```
* Make sure you're in your new virtual environment before installing packages or running scripts.

# Status

* This is a work in progress. The API and packaging are not stable.
* It is known that some boundary conditions lead to solver failures.
* The Python interface uses the same underlying .a compiled library as the ROS interface, so any issues related to the solver will affect both. The Matlab interface uses a separate compiled .mex library.
