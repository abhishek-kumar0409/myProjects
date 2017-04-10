# from flask import Flask, redirect, url_for, jsonify, request
# import yaml, json, datetime, os
# app = Flask(__name__)
#from bson import json_util
import yaml
import os
import zipfile
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

jsonResponse = {'image': '', 'keyPair': '', 'network': '', 'vm_count': '', 'net_count': '', 'port_count': ''}
finalResponse = {'vm_count': '', 'data': ''}

def countOccurenceOfResources(d):
    if 'OS::Nova::Server' in d:
        yield d['OS::Nova::Server']
    '''
    for k in d:
        if isinstance(d[k], list):
           for i in d[k]:
               for j in fun(i):
                   yield j
    '''


def extract_zip_file(packagePath):
    '''
      This method accepts the filepath of zipped file and extracts \
      it to the current directory.
    '''
    zip_ref = zipfile.ZipFile(packagePath, 'r')
    zip_ref.extractall(packagePath)
    zip_ref.close()


def readHeatTemplate():
    tags = ['vm_image']
    try:
                #rootDir = '.'
                # rootFir = '.'
                response = []

        #for dirName, subdirList, fileList in os.walk(rootDir):
        #    print('**************Found directory: %s' % dirName)
        #    for fname in fileList:
        #        print "dirName :: ", dirName
        #        print "subdirList :: ", subdirList
         #       print "fileList :: ", fileList
                fileContents = {}
         #       if fname.endswith('yaml') or fname.endswith('yml'):
         #           print('File Name :: \t%s' % fname)
                with open('SampleHeatTemp.yaml', 'r') as stream:
                        try:

                            #fileContents[fname] = (yaml.load(stream))
                            fileContents['fileName'] = (yaml.load(stream))
                            response.append(fileContents)
                            print "Response :: ", response
                        except yaml.YAMLError as exc:
                            print (exc)

            # output = jsonify(response)
                output = response
                return output
    except Exception as e:
        print e
        import traceback;traceback.print_exc()


# @app.route('/filterTemplate')#, methods=['POST'])
def parseHeatTemplate():  # templateFileList):
    # packagePath = request.form['path']
    # extract_zip_file(packagePath)
    templateFileList = readHeatTemplate()
    tags = ['resources', 'OS::Nova::Server']
    print ("\n\nInside parse template method")
    try:
        count = 0
        temp_list = []
        print "Template File List : ", templateFileList
        if len(templateFileList) != 0:
            for templateFiles in templateFileList:
                print ("\nTemplate_Keys :: ", templateFiles.keys())
                for templateFile, templateContents in templateFiles.items():
                    print ("HEAT Template File Names :: ", templateFile)
                    # print ( "Template Contents :: ", templateContents)
                    if 'resources' in templateContents:
                        print ("Resources Tag exist")
                        print ("templateFileName.keys()------> ", templateContents.keys())
                        # print "\n\nResources Tags Contents :: ",templateContents.get('resources')
                        for resourceTags, resourceContents in templateContents.get('resources').items():

                            jsonResponse = {}

                            print ("\n================Resource Tags ====================\n", resourceTags,)
                            print ("\n================Resource Contents ==================\n", resourceContents)
                            if resourceContents['type'] == 'OS::Nova::Server':
                                print ("resourceContents['type'] == ", resourceContents['type'])
                                print ("OS::Nova::Server properties exists")
                                count = count + 1

                                print "=============Count ================", count
                                print (resourceContents.keys())
                                if 'properties' in resourceContents.keys():
                                    print ("Key", resourceContents['properties'].keys())
                                    print (
                                    "Image Name ----------> ", resourceContents['properties']['image']['get_param'])
                                    print ("Networks-----------------> ",
                                           resourceContents['properties']['networks'])#['get_param'])

                                    '''
                                     Finding the datatype of resource networks
                                    '''
                                    resource_network = resourceContents['properties']['networks']

                                    print ("KeyPair Name ---------------->",
                                           resourceContents['properties']['key_name']['get_param'])
                                    print ("Flavor Name --------------> ",
                                           resourceContents['properties']['flavor']['get_param'])
                                    print (
                                    "=================================================================================")
                                    image_params = templateContents['parameters'][resourceContents['properties'] \
                                        ['image']['get_param']]  # ['image']['get_param']
                                    print "Image Param :: ", image_params
                                    key_params = templateContents['parameters'][resourceContents['properties'] \
                                        ['key_name']['get_param']]  # ['image']['get_param']
                                    flavor_params = templateContents['parameters'][resourceContents['properties'] \
                                        ['flavor']['get_param']]

                                    network_list = []
                                    if isinstance(resource_network,str) :
                                        print "**************Network type is string ***"
                                        jsonResponse['network'] = resource_network
                                    else:
                                        if isinstance(resource_network,dict) :
                                            print "Network type is Dictionary"
                                            network_name = resource_network.get('get_param')     #templateContents['parameters'][resourceContents['properties']['networks']]#.get('get_params')]
                                            print "Inside Network Dict : ", network_name
                                            network_params = templateContents['parameters'][network_name]
                                            print "Network Parameters ::", network_params
                                            if 'default' in network_params.keys():
                                                jsonResponse['network'] = network_params['default']
                                            else:
                                                jsonResponse['network'] = "N/A"

                                        elif isinstance(resource_network,list) :
                                            network_values = []
                                            for index, element in enumerate(resource_network):
                                                if isinstance(element, dict):
                                                    for k,v in element.items():
                                                        if k == 'network':
                                                            print "@@@@@@@@@@@@@@@@@@@@", k, v
                                                            network_list.append(v.get('get_param'))
                                                            print "Network Lisst :: ", network_list

                                                        elif k == 'port':
                                                            print "Network type id Port"

                                                network_params = templateContents['parameters'][network_list[index]] #['net_01', 'net_02']
                                                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~", network_params
                                                network_values.append(network_params['default'])

                                            jsonResponse['network'] = network_values

                                    if 'default' in image_params.keys():
                                         jsonResponse['image'] = image_params['default']
                                    else:
                                        jsonResponse['image'] = "N/A"

                                    if 'default' in key_params.keys():
                                        jsonResponse['keyPair'] = key_params['default']
                                    else:
                                        jsonResponse['keyPair'] = "N/A"

                                    if 'default' in flavor_params.keys():
                                        jsonResponse['flavor'] = flavor_params['default']

                                    else:
                                        jsonResponse['flavor'] = "N/A"



                                    print "\n\n\n********************JSON RESPONSE :: ", jsonResponse

                                    temp_list.append(jsonResponse)

                            else:
                                print "OS::Nova::Server  properties do not exist"

                    else:
                        print "Resource Tag not found"
        else:
            print "Template List is empty..."
        '''
        temp_list = []
        for i in range(0, count):
            temp_list.append(jsonResponse)
        '''
        print "Temp_list :------------------->>>>>>>> ", temp_list

        finalResponse['vm_count'] = temp_list.__len__()
        finalResponse['data'] = temp_list
        print  finalResponse
        # output = jsonify(jsonResponse)
        # output = jsonify(temp_list)
        # return output


    except Exception as e:
        print "Exception caught in {0}".format(e)
        import traceback;
        traceback.print_exc()


# templateContent = readHeatTemplate()

# for item in templateContent:
#     count = list(countOccurenceOfResources(item))
#     print ">>>>>>>>>>>>count>>>>>>>>>>>>", count
parseResponse = parseHeatTemplate()
#print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", parseResponse
#print "Output", parseResponse

# print result
'''
#if __name__=='__main__':
#    app.run('0.0.0.0',8085, debug = True)
'''
