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

from .base import Base
from .config.client import docker_api_client


class Publish(Base):
    """
    The publisher. Publish our image.
    """

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

        login = docker_api_client.login(
            self.auth_config["username"],
            password=self.auth_config["token"],
            email=self.auth_config["email"],
            registry=self.registry,
            reauth=True,
        )

        # logging.info("Loging status: %s", login)

        our_filter = {"reference": "pyfunceble"}

        if "docker.io" in self.build_method_args["tag"]:
            image_name = self.build_method_args["tag"][
                self.build_method_args["tag"].find("/") + 1 :
            ].split(":")[0]
        else:
            image_name = self.build_method_args["tag"].split(":")[0]

        images = docker_api_client.images(image_name, filters=our_filter)

        if "docker.io" in self.registry:
            tag_to_look_for = "/".join(self.build_method_args["tag"].split("/")[1:])
        else:
            tag_to_look_for = self.build_method_args["tag"]

        image_to_publish = []

        logging.debug("Images (found):\n%s", images)

        for image in images:
            logging.debug("Checking:\n%s", image)
            if "RepoTags" not in image:
                logging.debug("No repo tags found, continue.")
                continue

            if any([tag_to_look_for in x for x in image["RepoTags"]]):
                logging.info(
                    "Tag to look for (%s) found in repo tags (%s).",
                    tag_to_look_for,
                    image["RepoTags"],
                )
                image_to_publish.append(image.copy())
                continue

            logging.info(
                "Tag to look for (%s) not found in repo tags (%s).",
                tag_to_look_for,
                image["RepoTags"],
            )

        if not image_to_publish:
            raise RuntimeError("Image to publish not found!")

        logging.info("Started to publish.")

        for image in image_to_publish:
            if not self.are_we_authorized_to_push(image):
                logging.info(
                    "Skipping because we are not authorized to push. %s",
                    image["RepoTags"],
                )
                continue

            for repo_tag in image["RepoTags"]:
                if "docker.io" in self.registry and self.registry not in repo_tag:
                    repo_tag = f"{self.registry}/{repo_tag}"

                if self.registry not in repo_tag:
                    logging.info(
                        "Skipping %s because it does not match the registry.",
                        repo_tag,
                    )
                    continue

                logging.info("Publishing %s", repo_tag)
                publisher = docker_api_client.push(
                    repo_tag,
                    stream=True,
                    decode=True,
                )

                for response in publisher:
                    self.log_response(response)

        logging.info("Finished to publish.")
