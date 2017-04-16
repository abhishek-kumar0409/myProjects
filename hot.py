# from flask import Flask, redirect, url_for, jsonify, request
# import yaml, json, datetime, os
# app = Flask(__name__)
# from bson import json_util
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


class HeatTemplateParser:
    def extract_zip_file(self, packagePath):
        '''
        This method accepts the filepath of zipped file and extracts \
        it to the current directory.
        '''
        zip_ref = zipfile.ZipFile(packagePath, 'r')
        zip_ref.extractall(packagePath)
        zip_ref.close()

    def readHeatTemplate(self):
        tags = ['vm_image']
        try:
            rootDir = '.'
            # rootFir = '.'
            response = []

            for dirName, subdirList, fileList in os.walk(rootDir):
                for fname in fileList:
                    logger.debug("Directories Name : {0} ".format(dirName))
                    logger.debug("Sub Directories : {0} ".format(subdirList))
                    logger.debug("File Names : {0} ".format(fileList))
                    fileContents = {}
                    if fname.endswith('yaml') or fname.endswith('yml'):
                        logger.debug("Parsing '{0}' file in {1} directory..".format(fname, dirName))
                        with open(dirName + "/" + fname, 'r') as stream:
                            try:
                                fileContents[fname] = (yaml.load(stream))
                                response.append(fileContents)
                                print "********************************************************Response :: ", response
                            except yaml.YAMLError as exc:
                                print (exc)
                                import traceback;
                                traceback.print_exc()

                    else:
                        logger.debug("Skipping the parsing of {0} file ".format(fname))

            output = response
            return output
        except Exception as e:
            print e
            import traceback;
            traceback.print_exc()

    def parseHeatTemplate(self):
        # packagePath = request.form['path']
        # extract_zip_file(packagePath)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",
        templateFileList = self.readHeatTemplate()
        tags = ['resources', 'OS::Nova::Server']
        logger.debug("Waiting for the parsing results...")
        try:
            count = 0
            temp_list = []
            logger.debug("List of Heat Templates  : {0} ".format(templateFileList))
            if len(templateFileList) != 0:
                for templateFiles in templateFileList:
                    logger.debug("\nKeys in Template List :: {0} ".format((templateFiles.keys())))
                    for templateFile, templateContents in templateFiles.items():
                        logger.debug("HEAT Template File Names : {0} ".format(templateFile))
                        # print ( "Template Contents :: ", templateContents)

                        if 'resources' in templateContents:
                            logger.debug("Resources Metadata exist in {0}".format(templateFile))
                            logger.debug(
                                "Keys present in the TemplateContent Dicts : {0} ".format(templateContents.keys()))
                            # print "\n\nResources Tags Contents :: ",templateContents.get('resources')
                            resources_keys = templateContents.get('resources').keys()
                            print "&&&&BResources KEYS --------------------> ", resources_keys, templateContents.get('resources').items()
                            for resourceTags, resourceContents in templateContents.get('resources').items():

                                jsonResponse = {}

                                logger.debug(
                                    "=========Resource Tags -K-E-Y-S-> {0} -V-A-L-U-E-S-> {1} ======= ".format(
                                        resourceTags, resourceContents))
                                # logger.debug (
                                # "============Resource Contents ============\n {0}".format( resourceContents ))

                                if resourceContents['type'] == 'OS::Nova::Server':
                                    logger.debug('Match of Resource Type "OS::Nova::Server" found !!')
                                    count = count + 1

                                    logger.debug(
                                        "Total Number of Servers Present : {0}".format(count))
                                    logger.debug(
                                        "Total Number of Resources Tags : {0}".format(resourceContents.keys()))

                                    if 'properties' in resourceContents.keys():
                                        logger.debug("List of Property Tags : {0} ".format(
                                            resourceContents['properties'].keys()))
                                        logger.debug(
                                            "Image Name ----------> {0} ".format(
                                                resourceContents['properties']['image']['get_param']))
                                        logger.debug(
                                            "Networks-----------------> {0} ".format(
                                                resourceContents['properties']['networks']))

                                        '''
                                         Finding the datatype of resource networks
                                        '''

                                        #                                        logger.debug ("KeyPair Name ---------------->   {0}".format(
                                        #                                               resourceContents['properties']['key_name']['get_param']))
                                        logger.debug("Flavor Name -------------->   {0}".format(
                                            resourceContents['properties']['flavor']['get_param']))
                                        logger.debug(
                                            "=====================================================================")
                                        image_params = templateContents['parameters'][resourceContents['properties']\
                                            ['image']['get_param']]  # ['image']['get_param']
                                        logger.debug("Image Param :: {0} ".format(image_params))

                                        if 'key_name' in resourceContents['properties'].keys():
                                            logger.debug("KeyPair Name ---------------->   {0}".format(
                                                resourceContents['properties']['key_name']['get_param']))

                                            key_params = templateContents['parameters'][resourceContents['properties'] \
                                                ['key_name']['get_param']]  # ['image']['get_param']

                                            if 'default' in key_params.keys():
                                                jsonResponse['keyPair'] = key_params['default']
                                            else:
                                                jsonResponse['keyPair'] = "N/A"

                                        flavor_params = templateContents['parameters'][resourceContents['properties'] \
                                            ['flavor']['get_param']]

                                        resource_network = resourceContents['properties']['networks']
                                        network_list = []
                                        port_list = []
                                        if isinstance(resource_network, str):
                                            logger.debug("***** Data type of Network property is string *****")
                                            jsonResponse['network'] = resource_network
                                        else:

                                            if isinstance(resource_network, dict):
                                                logger.debug("****** Data type of Network property is Dictionary")
                                                network_name = resource_network.get('get_param')
                                                # templateContents['parameters'][resourceContents['properties']\
                                                # ['networks']]#.get('get_params')]

                                                logger.debug(" Network Dictionary Itemes : {0} ".format(network_name))
                                                network_params = templateContents['parameters'][network_name]
                                                logger.debug(" Network Parameters : {0} ".format(network_params))

                                                if 'default' in network_params.keys():
                                                    jsonResponse['network'] = network_params['default']
                                                else:
                                                    jsonResponse['network'] = "N/A"

                                            elif isinstance(resource_network, list):
                                                network_values = []
                                                port_values = []
                                                net_resource_values = []
                                                for index, element in enumerate(resource_network):
                                                    if isinstance(element, dict):
                                                        for k, v in element.items():
                                                            if k == 'network':
                                                                print "Network resources :-->", k, v
                                                                network_list.append(v.get('get_param'))
                                                                print "Network List :: ", network_list
                                                                network_params = templateContents['parameters'] \
                                                                    [network_list[index]]  # ['net_01', 'net_02']
                                                                logger.debug(
                                                                    " Network Parameters : {0}".format(network_params))
                                                                network_values.append(network_params['default'])

                                                                jsonResponse['network'] = network_values


                                                            elif k == 'port':
                                                                #print resource_network
                                                                logger.debug("Network type id =  Port")
                                                                if isinstance(element, dict):
                                                                    for k, v in element.items():
                                                                        print "------------------->Port  Key --> value-  -->", k, v

                                                                        if 'get_resource' in v.keys():
                                                                            for port_name in v.values():
                                                                                print "Port_Name :: ", port_name
                                                                                port_values.append(port_name)
                                                                                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", port_values
                                                                                print "----------->Resource Tags ::-----> ", resourceTags
                                                                                print "************PORT VALUES************", port_values
                                                                                if port_name in templateContents.get(
                                                                                        'resources').keys():
                                                                                    print "----------INside Port--------------------->",
                                                                                    port_properties = (
                                                                                    templateContents['resources'][
                                                                                        port_name]['properties'])
                                                                                    # net_list = []
                                                                                    for port_property_keys, port_property_values in port_properties.items():
                                                                                        if 'network' == port_property_keys:
                                                                                            print "port_values === ", port_property_values
                                                                                            for port_keys_1, port_values_1 in port_property_values.items():
                                                                                                print "Port_Values :: ", port_values_1
                                                                                                if port_keys_1 == 'get_resource':
                                                                                                    print "Resources..."
                                                                                                    print "Port_values -----------> ", port_values_1
                                                                                                    if port_values_1 in resources_keys:
                                                                                                        print "PPPPPPPPPPPPPPPPPPPPPPPPP-->", templateContents.get('resources')[port_values_1]
                                                                                                        if 'properties' in templateContents.get('resources')[port_values_1].keys():
                                                                                                            # Iterate for k, v if multiple properties found
                                                                                                            print "New Network Name :: ->", templateContents.get('resources')[port_values_1]['properties']['name']
                                                                                                            network_list.append(templateContents.get('resources')[port_values_1]['properties']['name'])
                                                                                                            net_resource_values = (
                                                                                                                templateContents.get(
                                                                                                                    'resources')[
                                                                                                                    port_values_1][
                                                                                                                    'properties'][
                                                                                                                    'name'])
                                                                                                        else:
                                                                                                            net_resource_values = "New_network"

                                                                                                        print "^^^^^^^^^^^^Network List array in Get_resource", network_list

                                                                                                        #for i in network_list:
                                                                                                            #net_resource_values.append(i)
                                                                                                        print "^^^^^^^^^^^^Network values in get_resource", net_resource_values
                                                                                                        network_values.append(net_resource_values)


                                                                                                    else:
                                                                                                        print "Index -----------> ", index
                                                                                                        network_params = \
                                                                                                        templateContents[
                                                                                                            'parameters'] \
                                                                                                            [
                                                                                                            network_list[
                                                                                                                index]]  # ['net_01', 'net_02']
                                                                                                        logger.debug( \
                                                                                                            " Network Parameters : {0}".\
                                                                                                                format(
                                                                                                                network_params))
                                                                                                        print "Network Paramsmmm --> ", network_params
                                                                                                        network_values.append(
                                                                                                            network_params[
                                                                                                                'default'])

                                                                                                        jsonResponse[
                                                                                                            'network'] = network_values


                                                                                                        # print v.values()
                                                                                                elif port_keys_1 == 'get_param':
                                                                                                    print "Parameters ......."
                                                                                                    network_list.append(
                                                                                                        port_values_1)
                                                                                                    print "Network _ list ---- > ", network_list
                                                                                                    print "Index in get_param section :: --->", network_list[index]
                                                                                                    network_params = templateContents['parameters'][network_list[index]]  # ['net_01', 'net_02']
                                                                                                    logger.debug(
                                                                                                        " Network Parameters : {0}". \
                                                                                                            format(
                                                                                                            network_params))
                                                                                                    network_values.append(
                                                                                                        network_params[
                                                                                                            'default'])

                                                                                                    jsonResponse[
                                                                                                        'network'] = network_values

                                                                            print "########################", network_values
                                                                        else:
                                                                            pass
                                                                            # if resourceTags in port_values:

                                                                            #     network_params = resources[]
                                                              #  jsonResponse['network'] = "N/A because of Ports !!"


                                                                # network_params = templateContents['parameters'][network_list[index]] #['net_01', 'net_02']
                                                                # logger.debug ( " Network Parameters : {0}".format ( network_params ) )
                                                                # network_values.append(network_params['default'])

                                                jsonResponse['network'] = network_values

                                        if 'default' in image_params.keys():
                                            jsonResponse['image'] = image_params['default']
                                        else:
                                            jsonResponse['image'] = "N/A"

                                        # if 'default' in key_params.keys():
                                        #                                            jsonResponse['keyPair'] = key_params['default']
                                        #                                        else:
                                        #                                            jsonResponse['keyPair'] = "N/A"

                                        if 'default' in flavor_params.keys():
                                            jsonResponse['flavor'] = flavor_params['default']

                                        else:
                                            jsonResponse['flavor'] = "N/A"

                                        logger.debug(
                                            "\n\n\n********************JSON RESPONSE :: {0}************************* ".format(
                                                jsonResponse))

                                        temp_list.append(jsonResponse)

                                else:
                                    logger.debug("OS::Nova::Server  properties do not exist")

                        else:
                            logger.debug("Resource Tag not found in the {0} templateFile ".format(templateFile))
            else:
                logger.debug("Template List is empty...")
            '''
            temp_list = []
            for i in range(0, count):
                temp_list.append(jsonResponse)
            '''
            logger.debug("List of JSONs :--> {0}".format(temp_list))

            finalResponse['vm_count'] = temp_list.__len__()
            finalResponse['data'] = temp_list
            logger.info("Final Response : {0}".format(finalResponse))

            return finalResponse


        except Exception as e:
            logger.exception(" Exception caught in {0}".format(e))
            import traceback;
            traceback.print_exc()


ht = HeatTemplateParser()
# templateContent = readHeatTemplate()

# for item in templateContent:
#     count = list(countOccurenceOfResources(item))
#     print ">>>>>>>>>>>>count>>>>>>>>>>>>", count
parseResponse = ht.parseHeatTemplate()
# print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", parseResponse
# print "Output", parseResponse

# print result
'''
#if __name__=='__main__':
#    app.run('0.0.0.0',8085, debug = True)
'''
