from flask import Flask, redirect, url_for, jsonify, request
import yaml, json, datetime, os
app = Flask(__name__)
#from bson import json_util
import yaml
import os
import zipfile
import logging
#from HeatTemplateParserObj import HeatTemplateParser
from HeatTemplateParser_latest import HeatTemplateParser

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

jsonResponse = {'image': '', 'keyPair': '', 'network': '', 'vm_count': '', 'net_count': '', 'port_count': ''}
finalResponse = {'vm_count': '', 'data': ''}


@app.route('/parseTemplate')#, methods=['POST'])
def parse_heat_template():  # templateFileList):
    try:
        print "H(IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
        
        # packagePath = request.form['path']
        # extract_zip_file(packagePath)
        #templateFileList = self.readHeatTemplate()
        #tags = ['resources', 'OS::Nova::Server']
        ht = HeatTemplateParser()
        response = ht.parseHeatTemplate()    
        output = jsonify(response)
        # output = jsonify(temp_list)
        return output


    except Exception as e:
        logger.exception(" Exception caught in {0}".format(e) )
        import traceback; traceback.print_exc()

if __name__=='__main__':
    app.run('0.0.0.0',8085, debug = True)

