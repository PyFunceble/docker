#!/bin/bash

set -e

USER_ID=${LOCAL_USER_ID:-9001}

if [[ -z $(grep -E "pyfunceble:x:${USER_ID}" /etc/passwd) ]]
then
    if [[ ! -d /home/pyfunceble ]]
    then
        useradd --shell /bin/bash -u $USER_ID -o -c "PyFunceble user" -m pyfunceble
    else
        useradd --shell /bin/bash -u $USER_ID -o -c "PyFunceble user" pyfunceble
    fi
fi

export HOME=/home/pyfunceble
export PYFUNCEBLE_BASE_DIR="${HOME}"
export PYFUNCEBLE_CONFIG_DIR="${PYFUNCEBLE_BASE_DIR}/config"
export PYFUNCEBLE_RUN_DIR="${PYFUNCEBLE_BASE_DIR}/run"
export PYFUNCEBLE_FILES_DIR="${PYFUNCEBLE_BASE_DIR}/files"

export PYFUNCEBLE_AUTO_CONFIGURATION="YES"
export PYFUNCEBLE_CONFIG_DIR="${PYFUNCEBLE_CONFIG_DIR}"


if [[ "${1:0:1}" == "/" ]]
then
    exec gosu pyfunceble ${@}
else
    exec gosu pyfunceble /usr/local/bin/pyfunceble.sh ${@}
fi