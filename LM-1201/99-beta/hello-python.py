#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DevNet Express - Hello Python!

Running this script will help you verify that your Python environment is setup
correctly.  It will display information about your Python environment including
the location of your Python interpreter, where your `pip install ...` packages
are being installed and more.

Usage:
    python hello-python.py

"""


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"


import os
import sys

import setuptools


PLATFORM = sys.platform
PYTHON_INTERPRETER = sys.executable
IMPLEMENTATION = sys.implementation.name
VERSION = sys.implementation.version
SITE_PACKAGES_DIRECTORY = setuptools.distutils.sysconfig.get_python_lib()
EXEC_DIRECTORY = os.path.dirname(sys.exec_prefix)
IN_VIRTUAL_ENVIRONMENT = (
        hasattr(sys, "real_prefix") and sys.exec_prefix != sys.real_prefix
)


platform_friendly_names = {
    "linux": "Linux",
    "win32": "Windows",
    "cygwin": "Windows/Cygwin",
    "darwin": "macOS",
}


def platform_friendly_name():
    """Use friendly platform names, if available."""
    if PLATFORM in platform_friendly_names:
        return platform_friendly_names[PLATFORM]
    else:
        return PLATFORM


def pretty_version():
    """Format version data into a pretty version number."""
    return "{major}.{minor}.{micro}".format(
        major=VERSION.major,
        minor=VERSION.minor,
        micro=VERSION.micro,
    )


def interpreter_is_good():
    """Check the implementation and version of the Python interpreter."""
    return IMPLEMENTATION == "cpython" and \
           VERSION.major == 3 and VERSION.minor >= 5


def main():
    """This function is called when the script is executed.

    See the `if _name_ == "main:"` conditional below.

    """
    print("🐍  Welcome to Python!\n")

    # Display the location of the current Python interpreter
    print(
        "Your Python interpreter is located here:\n"
        "    {interpreter}\n"
        "".format(
            interpreter=PYTHON_INTERPRETER,
        )
    )

    # Display the interpreter info and lab compatibility
    print(
        "It looks like you are running {implementation} version {version} on "
        "{platform}!"
        "".format(
            implementation=IMPLEMENTATION,
            version=pretty_version(),
            platform=platform_friendly_name(),
        ),
        end='',
    )
    if interpreter_is_good():
        print("  😎  #Awesome\n")
    else:
        print("  ⚠️  For our labs you will need to use CPython 3.5+.\n")

    # Check to see if we are running in a virtual environment
    if IN_VIRTUAL_ENVIRONMENT:
        print("I see that you have activated your virtual environment! ✅\n")
    else:
        print(
            "It looks like you haven't activated your virtual environment.  ☹️"
        )
        venv_created_answer = input("Did you create one?\n[y/n]")
        if venv_created_answer.strip().lower().startswith("y"):
            print("\n⚠️  Activate your virtual environment by running:")
            if PLATFORM == "win32":
                print("    <virtual-environment-name>\\Scripts\\activate.bat")
            else:
                print("    source <virtual-environment-name>/bin/activate")
        else:
            print(
                "\n⚠️  Follow the lab instructions to setup your virtual "
                "environment."
            )
        sys.exit()

    # Show where pip installed packages and scripts can be found
    print(
        "Any packages you install with `pip install` will be installed to:\n"
        "    {site_packages_directory}\n"
        "\n"
        "Executable scripts will be found here:\n"
        "    {exec_directory}\n\n"
        "".format(
            site_packages_directory=SITE_PACKAGES_DIRECTORY,
            exec_directory=EXEC_DIRECTORY,
        )
    )


if __name__ == '__main__':
    main()
