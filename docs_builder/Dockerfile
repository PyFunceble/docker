ARG PYTHON_VERSION="latest"

FROM python:${PYTHON_VERSION} as builder

ARG PYFUNCEBLE_REPO="https://github.com/funilrys/PyFunceble.git"
ARG COMMIT_ID="dev"

ENV PYFUNCEBLE_REPO=${PYFUNCEBLE_REPO}
ENV COMMIT_ID=${COMMIT_ID}

RUN apt update  && \
    apt -y --no-install-recommends install git

RUN mkdir -p /pyfunceble && \
    pip install --upgrade pip && \
    git clone ${PYFUNCEBLE_REPO} /pyfunceble && \
    git -C /pyfunceble checkout ${COMMIT_ID} && \
    cd /pyfunceble && \
    pip3 install .[docs] && \
    python3 docs/gen_ref_pages.py && \
    mkdocs build && \
    find /pyfunceble -mindepth 1 -maxdepth 1 -type d -not -name site -exec rm -rf '{}' \;

FROM docker.io/nginx:stable

COPY --from=builder /pyfunceble/site /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
