#!/bin/bash

set -e

for environmentName in $(env | cut -d "=" -f1)
do
    lowerEnvName=${environmentName,,}

    if [[ ${lowerEnvName:0:10} == "pyfunceble" && ${lowerEnvName: -3} == "dir" ]]
    then
        if [[ ! -d ${!environmentName} ]]
        then
            mkdir -p ${!environmentName}
            touch ${!environmentName}/.keep
        fi
    fi
done

cd ${PYFUNCEBLE_RUN_DIR}

PyFunceble ${@}

cd ${OLDPWD}