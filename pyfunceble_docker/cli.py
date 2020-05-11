"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This file is part of the PyFunceble project.

Provides the CLI entrypoints.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2019, 2020 PyFunceble
    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import argparse
import logging

from . import VERSION
from .build import Build
from .publish import Publish


def add_common_commands(parser):
    """
    Adds some common commands to the given parser.
    """

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version and exit.",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Activated the debug mode.",
        action="store_true",
        default=False,
    )

    parser.add_argument("-b", "--build-dir", type=str, help="Sets the build directory.")

    parser.add_argument(
        "--pyfunceble-version", help="Sets the PyFunceble version to build.", type=str,
    )

    parser.add_argument(
        "-p", "--pkg-name", help="Sets the name of the package to install.", type=str,
    )

    parser.add_argument(
        "--python-version", help="Sets the Python version to install.", type=str
    )

    return parser


def builder():
    """
    Provides the builder CLI.
    """

    if __name__ == "pyfunceble_docker.cli":
        parser = argparse.ArgumentParser(
            description="The PyFunceble docker (image) builder."
        )

        add_common_commands(parser)

        parser.add_argument(
            "--publish",
            help="Allow us to publish the built image.",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--is-latest",
            help="Tell us that the image is the latest one.",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "-c", "--commit", help="Sets the commit to use as package.", type=str
        )

        args = parser.parse_args()

        if args.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s::%(levelname)s::%(filename)s:%(lineno)s] %(message)s",
            )
        else:
            logging.basicConfig(
                level=logging.INFO, format="[%(asctime)s::%(levelname)s] %(message)s"
            )

        logging.debug("ARGS:\n%s", args)

        Build(
            args.build_dir,
            version=args.pyfunceble_version,
            pkg_name=args.pkg_name,
            python_version=args.python_version,
            is_latest=args.is_latest,
            commit=args.commit,
        ).it()

        if args.publish:
            Publish(
                args.build_dir,
                version=args.pyfunceble_version,
                pkg_name=args.pkg_name,
                python_version=args.python_version,
                is_latest=args.is_latest,
                commit=args.commit,
            ).it()


def publisher():
    """
    Provides the publisher CLI.
    """

    if __name__ == "pyfunceble_docker.cli":
        parser = argparse.ArgumentParser(
            description="The PyFunceble docker (image) publisher."
        )

        add_common_commands(parser)

        args = parser.parse_args()

        if args.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s::%(levelname)s::%(filename)s:%(lineno)s] %(message)s",
            )
        else:
            logging.basicConfig(
                level=logging.INFO, format="[%(asctime)s::%(levelname)s] %(message)s"
            )

        logging.debug("ARGS:\n%s", args)

        Publish(
            args.build_dir,
            version=args.pyfunceble_version,
            pkg_name=args.pkg_name,
            python_version=args.python_version,
        ).it()
