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

Provides the base of all our master classes.

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

    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024 Nissar Chababy
    Copyright (c) 2019, 2020, 2021, 2022, 2023, 2024 PyFunceble Contributors

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

import logging
import os
from typing import Optional

import requests

from .config.client import REGISTRY_URL


class Base:
    """
    Our base class.
    """

    # pylint: disable=too-many-arguments

    image_namespace: str = "pyfunceble"
    docker_repository: str = ""

    version: str = ""
    pkg_name: str = "PyFunceble"
    python_version: str = "latest"
    branch: str = "master"
    package_archive: str = "https://github.com/funilrys/PyFunceble/archive/%s.zip"

    python2docker_arg = {
        "version": "PYFUNCEBLE_VERSION",
        "pkg_name": "PYFUNCEBLE_PKG_NAME",
        "python_version": "PYTHON_VERSION",
        "package_archive": "PACKAGE_ARCHIVE_URL",
    }

    is_latest: bool = False

    build_dir: str = ""

    build_args: dict = {}

    build_method_args: dict = {
        "path": "",
        "quiet": False,
        "rm": True,
        "pull": False,
        "decode": True,
        "tag": f"{image_namespace}/",
    }

    def __init__(
        self,
        build_dir: str,
        version: Optional[str] = None,
        pkg_name: Optional[str] = None,
        python_version: Optional[str] = None,
        is_latest: bool = False,
        commit: Optional[str] = None,
    ) -> None:

        try:
            if not os.path.isdir(build_dir):
                raise FileNotFoundError(build_dir)
        except TypeError:
            raise Exception(f"<build_dir> should be {str}.")

        if version:
            self.version = version

        if pkg_name:
            self.pkg_name = pkg_name

        if python_version:
            self.python_version = python_version

        if self.pkg_name.lower().endswith("dev"):
            self.branch = "dev"
        else:
            self.branch = "master"

        if commit:
            self.package_archive = self.package_archive % commit

        self.is_latest = is_latest
        self.docker_repository = f"{self.image_namespace}/{self.pkg_name.lower()}"

        self.build_args.update(self.get_build_args())

        self.build_method_args["buildargs"] = self.build_args
        self.build_method_args["path"] = build_dir
        self.build_method_args[
            "tag"
        ] = f"{REGISTRY_URL}/{self.docker_repository}:{self.version.lower()}"

        logging.debug("VERSION: %s", self.version)
        logging.debug("PKG Name: %s", self.pkg_name)
        logging.debug("Python Version: %s", self.python_version)
        logging.debug("Build Args:\n%s", self.build_args)
        logging.debug("Build Method args:\n%s", self.build_method_args)

    def get_build_args(self) -> dict:
        """
        Provides the build arguments.
        """

        result = dict()

        for local, upstram in self.python2docker_arg.items():
            if hasattr(self, local):
                result[upstram] = getattr(self, local)

        return result

    @classmethod
    def log_response(cls, response: dict):
        """
        Given a response from the Docker client.
        We log it.
        """

        if "stream" in response:
            for line in response["stream"].splitlines():
                if line:
                    logging.info(line)

        if "progressDetail" in response and "status" in response:
            if "id" in response and response["progressDetail"]:
                percentage = round(
                    (response["progressDetail"]["current"] * 100)
                    / response["progressDetail"]["total"],
                    2,
                )

                logging.info(
                    "%s (%s): %s/%s (%s%%)",
                    response["status"],
                    response["id"],
                    response["progressDetail"]["current"],
                    response["progressDetail"]["total"],
                    percentage,
                )
            elif "id" in response:
                logging.info("%s (%s)", response["status"], response["id"])
            else:
                logging.info("%s", response["status"])
        elif "errorDetail" in response and response["errorDetail"]:
            raise Exception(response["errorDetail"]["message"])
        elif "status" in response:
            logging.info("%s", response["status"])

    def is_already_pushed(self, tag: str):
        """
        Checks if the given tag was already pushed.
        """

        url = f"https://registry.hub.docker.com/v2/repositories/{self.docker_repository}/tags/"

        tag_published = False

        while True:
            req = requests.get(url)
            req.raise_for_status()

            data = req.json()

            tag_published = any([x["name"] == tag for x in data["results"]])

            if not tag_published and "next" in data and data["next"]:
                url = data["next"]
            else:
                break

        logging.debug("Tag published: %s", tag_published)

        return tag_published
