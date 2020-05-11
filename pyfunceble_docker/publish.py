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

Provides the publisher.

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

import logging
import os

from .base import Base
from .config.client import docker_api_client


class Publish(Base):
    """
    The publisher. Publish our image.
    """

    auth_config: dict = {"username": "", "password": "", "email": ""}

    def it(self) -> None:  # pylint: disable=invalid-name
        """
        Publish the image
        """

        logging.info("Started to publish.")

        if "OUR_DOCKER_USERNAME" not in os.environ:
            raise Exception("OUR_DOCKER_USERNAME not found.")

        if "OUR_DOCKER_PASSWORD" not in os.environ:
            raise Exception("OUR_DOCKER_PASSWORD not found.")

        if "OUR_DOCKER_EMAIL" not in os.environ:
            raise Exception("OUR_DOCKER_EMAIL not found.")

        self.auth_config["username"] = os.environ["OUR_DOCKER_USERNAME"]
        self.auth_config["passowrd"] = os.environ["OUR_DOCKER_PASSWORD"]
        self.auth_config["email"] = os.environ["OUR_DOCKER_EMAIL"]

        our_filter = {"reference": "pyfunceble"}

        images_name = f"{self.image_namespace}/{self.pkg_name.lower()}"
        images = docker_api_client.images(images_name, filters=our_filter)
        tag_to_look_for = self.build_method_args["tag"].split("/")[-1]

        image_to_publish = []

        logging.debug("Images (found):\n%s", images)

        for image in images:
            logging.debug("Checking:\n%s", image)
            if "RepoTags" not in image:
                logging.debug("No repo tags found, continue.")
                continue

            if any([tag_to_look_for in x for x in image["RepoTags"]]):
                logging.debug(
                    "Tag to look for (%s) found in repo tags (%s).",
                    tag_to_look_for,
                    image["RepoTags"],
                )
                image_to_publish.append(image.copy())
                continue

            logging.debug(
                "Tag to look for (%s) not found in repo tags (%s).",
                tag_to_look_for,
                image["RepoTags"],
            )

        if not image_to_publish:
            raise Exception("Image to publish not found!")

        login = docker_api_client.login(
            self.auth_config["username"], password=self.auth_config["password"]
        )

        logging.info("Loging status: %s", login)

        repository_to_publish_into = self.build_method_args["tag"].split(":")[0]

        logging.debug("Repository to publish into: %s", repository_to_publish_into)

        for image in image_to_publish:
            publisher = docker_api_client.push(
                repository_to_publish_into,
                stream=True,
                decode=True,
                auth_config=self.auth_config,
            )

            for response in publisher:
                self.log_response(response)

        logging.info("Finished to publish.")
