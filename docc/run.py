#
# start the server
#

import sys, service, json

from bottle import run

if len(sys.argv) > 1:
    conf_file_path = sys.argv[1]
    conf_file = open(conf_file_path).read()
     
    confJson = {}
    confJson = json.loads(conf_file)
    
    print 'Starting bottle service at \nhost:%s \nport:%s' % (confJson['docc.host'], confJson['docc.bottle.port']) 
    
    # Initialize service objects
    service.setup()
    run(host=confJson['docc.host'], port=confJson['docc.bottle.port'])
    
else:
    print 'Config file not specified:'
    print "usage:", sys.argv[0],"[conf file]"

