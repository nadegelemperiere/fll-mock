#!/bin/bash
# -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Script to launch robotframework tests on common python
# classes
# -------------------------------------------------------
# Nadège LEMPERIERE, @01 november 2022
# Latest revision: 01 november 2022
# --------------------------------------------------- """

# Retrieve absolute path to this script
script=$(readlink -f $0)
scriptpath=`dirname $script`

# Parse arguments from flags
args=""
key=""
while getopts s:l:d:k: flag
do
    case "${flag}" in
          s) args+=" --suite ${OPTARG}";;
          l) args+=" --loglevel ${OPTARG}";;
          d) args+=" --log ${OPTARG}/log.html --report ${OPTARG}/report.html";;
          k) key=${OPTARG}
    esac
done

# Install required python packages
pip install --quiet --no-warn-script-location -r $scriptpath/../requirements-test.txt
pip install --quiet --no-warn-script-location -r $scriptpath/../requirements.txt
pip install --quiet  --no-warn-script-location $scriptpath/../

# Launch python scripts to setup terraform environment
python3 -m robot --variable data:$scriptpath/../test/data/                  \
                 $args                                                      \
                 $scriptpath/../test/cases