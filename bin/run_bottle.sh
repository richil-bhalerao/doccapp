#!/bin/bash
#
# Run our bottle service
#

# working direct to set the path to our modules 
export DOCC_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}/"/)" && cd .. && pwd )"

echo -e "\n** starting bottle service from $DOCC_HOME **\n"

# run
python ${DOCC_HOME}/docc/run.py ${DOCC_HOME}/conf/docc.conf
