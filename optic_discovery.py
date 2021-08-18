#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from ansible.module_utils.basic import *
import os, sys
from ansible.module_utils import PYSNMP_BASE_FUNC
from ansible.module_utils import BASE_FUNC
import time
import ast
import json
import argparse
import sys
from ncclient.xml_ import new_ele
from ncclient import manager
from lxml import etree



def get_optic_interface_name(connection):
    
    rpc = new_ele('get-interface-optics-diagnostics-information')
    xml_result = connection.rpc(rpc)
    connection.close_session()
    name_optic=[]
    interf_result = xml_result.xpath('//physical-interface/name')
    if interf_result:
        # for i in range(len(interf_result)):
            # a = str(interf_result[i])
        for interf in interf_result:
            a = str(interf.xpath("normalize-space(.)"))
            name_optic.append(a)      
       

    return name_optic


###############################################################################
def main():
    module = AnsibleModule(
        argument_spec=dict(host=dict(required=True, default=None, type="str"),  # host or ipaddr
                           UN=dict(required=True, type="str"),
                           PW=dict(required=True, type="str"),
                           Port=dict(required=True, type="int")
                           )
                          )
    args = module.params

    connection = None
    

    ###########################################################################  
    try:
        connection = manager.connect(host=args['host'], port = args['Port'], username = args['UN'], 
                                     password = args['PW'], device_params={'name':'junos'}, 
                                     timeout = 5, hostkey_verify=False)
    except:
        msg = "UNKNOWN: Authentication failed with provided arguments"
        print(msg)

    

    ###########################################################################
    if connection:
              
                    name = get_optic_interface_name(connection)
                    
                    data = dict()
                    data["list"] = name
                    data["json_string"] = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=True)
                    data['changed'] = True
                    data['failed'] = False
                    module.exit_json(**data)
            

###############################################################################    
if __name__ == "__main__":    
    main()
        










 














