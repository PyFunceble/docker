ARG PYTHON_VERSION="latest"

FROM python:${PYTHON_VERSION}

ARG PYFUNCEBLE_VERSION=""
ARG PYFUNCEBLE_PKG_NAME="PyFunceble"
ARG PACKAGE_ARCHIVE_URL=""

ENV PYFUNCEBLE_VERSION=${PYFUNCEBLE_VERSION}
ENV PYFUNCEBLE_PKG_NAME=${PYFUNCEBLE_PKG_NAME}
ENV PACKAGE_ARCHIVE_URL=${PACKAGE_ARCHIVE_URL}

RUN apt-get update  && \
    apt-get -y --no-install-recommends install ca-certificates curl && \
    apt-get install gosu

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY pyfunceble.sh /usr/local/bin/pyfunceble.sh

RUN chmod +x /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/pyfunceble.sh

RUN pip3 install "${PYFUNCEBLE_PKG_NAME}[all] @ ${PACKAGE_ARCHIVE_URL}"

ENTRYPOINT [ "entrypoint.sh" ]