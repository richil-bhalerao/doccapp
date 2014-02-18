#
# start the server
#

import sys, service, json

from bottle import run

#Add defaut values
docchost = "localhost"
doccbottleport = 8080

if len(sys.argv) > 1:
    conf_file_path = sys.argv[1]
    conf_file = open(conf_file_path).read()
     
    confJson = {}
    confJson = json.loads(conf_file)
    
    docchost = confJson['docc.host']
    doccbottleport = confJson['docc.bottle.port']
    
    print 'Starting bottle service at \nhost:%s \nport:%s' % (docchost, doccbottleport) 
    
    # Initialize service objects
    service.setup()
    run(host=docchost, port=doccbottleport)
    
else:
    print 'Config file not specified:'
    print "usage:", sys.argv[0],"[conf file]"

