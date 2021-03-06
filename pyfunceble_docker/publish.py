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
from .config.client import REGISTRY_URL, docker_api_client


class Publish(Base):
    """
    The publisher. Publish our image.
    """

    auth_config: dict = {"username": "", "password": "", "email": ""}

    def are_we_authorized_to_push(self, images: dict) -> bool:
        """
        Checks if we are authorized to push.
        """

        if "RepoTags" not in images or not images["RepoTags"]:
            return False

        for repo_tag in images["RepoTags"]:
            tag = repo_tag.split(":")[-1]

            if tag == "latest":
                continue

            if self.is_already_pushed(tag):
                return False
        return True

    def it(self) -> None:  # pylint: disable=invalid-name
        """
        Publish the image
        """

        if "OUR_DOCKER_USERNAME" not in os.environ:
            raise Exception("OUR_DOCKER_USERNAME not found.")

        if "OUR_DOCKER_PASSWORD" not in os.environ:
            raise Exception("OUR_DOCKER_PASSWORD not found.")

        if "OUR_DOCKER_EMAIL" not in os.environ:
            raise Exception("OUR_DOCKER_EMAIL not found.")

        self.auth_config["username"] = os.environ["OUR_DOCKER_USERNAME"]
        self.auth_config["password"] = os.environ["OUR_DOCKER_PASSWORD"]
        self.auth_config["email"] = os.environ["OUR_DOCKER_EMAIL"]

        login = docker_api_client.login(
            self.auth_config["username"],
            password=self.auth_config["password"],
            email=self.auth_config["email"],
            registry=REGISTRY_URL,
            reauth=True,
        )
        logging.info("Loging status: %s", login)

        our_filter = {"reference": "pyfunceble"}

        images = docker_api_client.images(self.docker_repository, filters=our_filter)
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

        logging.info("Started to publish.")

        for image in image_to_publish:
            if self.are_we_authorized_to_push(image):
                for repository in image["RepoTags"]:
                    repository = f"{REGISTRY_URL}/{repository}"

                    logging.info("Publishing %s", repository)
                    publisher = docker_api_client.push(
                        repository,
                        stream=True,
                        decode=True,
                        auth_config=self.auth_config,
                    )

                    for response in publisher:
                        self.log_response(response)

        logging.info("Finished to publish.")
