## Quick references

* **Where to file issues:** https://github.com/funilrys/PyFunceble/issues/new/choose
* **Where to get help:** https://keybase.io/team/pyfunceble
* **Where to get the documentation of PyFunceble-dev:** http://pyfunceble.readthedocs.io/en/dev/

## What is PyFunceble?

PyFunceble is the tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

Its main objective is to provide the availability of domains, IPs, and since recently URL by generating an accurate result based on results from WHOIS, NSLOOKUP, and HTTP status codes.

![logo](https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png)

## About this image

This image is automatically generated as soon as a new version is released from the [dev branch](https://github.com/funilrys/PyFunceble/tree/dev) of PyFunceble.

This image is intended to Provide PyFunceble-dev in a system-independent matter.

### How is it made?

Our CI deployment stage use [our very own builder](https://github.com/PyFunceble/docker) after each commit to the [dev branch](https://github.com/funilrys/PyFunceble/tree/dev) of PyFunceble.

Our very own builder is in charge of checking if the commit declares a new version. If it's the case, a new deployment to the Docker Hub will be done. Otherwise, nothing will be done.

### Environment Variables

* `LOCAL_USER_ID`: Tells the entry point which user ID to give to the `pyfunceble` user.

### Locations

* `/home/pyfunceble/config`: Is the equivalent of `${HOME}/.config/PyFunceble` if you already used PyFunceble before.
* `/home/pyfunceble/run`: Is where we move to start a test. It's also the location of the `output/` directory.

### How to run it ?


**Note**: In the following examples, `[PyFunceble parameters]` can be [any of the PyFunceble parameters](https://pyfunceble.readthedocs.io/en/dev/usage/index.html#global-overview). But if it starts with a slash (`/`), the entry point will try to run the given command. As an example, `/bin/bash` will provide the shell from inside the container.

**Warning**: All PyFunceble operations will be made as the `pyfunceble` user.

With the latest version:

```shell
docker run -it pyfunceble/pyfunceble-dev [PyFunceble parameters]
```

With the latest version and data persistence:

```shell
docker run -it -v ${PWD}/inside:/home/pyfunceble pyfunceble/pyfunceble-dev [PyFunceble parameters]
```

With the latest version, data persistence with the current user as the owner of the generated files:

```shell
docker run -it -v ${PWD}/inside:/home/pyfunceble pyfunceble/pyfunceble-dev -e LOCAL_USER_ID=`id -u ${USER}` [PyFunceble parameters]
```

With the latest version, data persistence and database persistence (MySQL/MariaDB DB Type)

```shell
docker run -it -v ${PWD}/inside:/home/pyfunceble -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock pyfunceble/pyfunceble-dev [PyFunceble parameters]
```

## License

```
MIT License

Copyright (c) 2020 PyFunceble
Copyright (c) 2020 Nissar Chababy

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
```