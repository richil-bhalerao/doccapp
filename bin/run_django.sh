#!/bin/bash
#
# Run our django service
#

# working direct to set the path to our modules
export DOCC_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}/"/)" && cd .. && pwd )"

echo -e "\n** starting django service from $DOCC_HOME **\n"


# run
python ${DOCC_HOME}/mysite/manage.py runserver
