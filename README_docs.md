## Quick references

* **Where to file issues:** https://github.com/funilrys/PyFunceble/issues/new/choose
* **Where to get help:** https://keybase.io/team/pyfunceble
* **Where to get the documentation of PyFunceble-dev:** http://pyfunceble.readthedocs.io/en/dev/

## What is PyFunceble?

PyFunceble is the tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

Its main objective is to provide the availability of domains, IPs, and since recently URL by generating an accurate result based on results from WHOIS, NSLOOKUP, and HTTP status codes.

![logo](https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png)

## About this image

This image is automatically generated as soon as a new version is released from the [switch-to-mkdocs branch](https://github.com/funilrys/PyFunceble/tree/swith-to-mkdocs) of PyFunceble.

This image is intended to Provide the documentation of the PyFunceble Project in a system-independent matter.

### How is it made?

Our CI deployment stage use [our very own builder](https://github.com/PyFunceble/docker) after each commit to the [switch-to-mkdocs branch](https://github.com/funilrys/PyFunceble/tree/switch-to-mkdocs) of PyFunceble.

Our very own builder is in charge of checking if the commit declares a new version. If it's the case, a new deployment to the Docker Hub will be done. Otherwise, nothing will be done.

### Environment Variables

* None

### How to run it ?


With the latest version:

```shell
docker run -it -p 8080:80 pyfunceble/docs
```

With the latest version and data persistence:

```shell
docker run -it -v ${PWD}/inside:/home/pyfunceble pyfunceble/pyfunceble-dev [PyFunceble parameters]
```

## License

```
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
```
