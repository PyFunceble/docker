ARG PYTHON_VERSION="latest"

FROM python:${PYTHON_VERSION}

ARG PYFUNCEBLE_VERSION=""
ARG PYFUNCEBLE_PKG_NAME="PyFunceble"

ENV PYFUNCEBLE_VERSION=${PYFUNCEBLE_VERSION}
ENV PYFUNCEBLE_PKG_NAME=${PYFUNCEBLE_PKG_NAME}

RUN apt-get update  && \
    apt-get -y --no-install-recommends install ca-certificates curl

RUN apt-get install gosu

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY pyfunceble.sh /usr/local/bin/pyfunceble.sh

RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/pyfunceble.sh

RUN pip3 install ${PYFUNCEBLE_PKG_NAME}===${PYFUNCEBLE_VERSION}

ENTRYPOINT [ "entrypoint.sh" ]