from jnpr.junos import Device
from collections import defaultdict

def xml_element_to_dict(tree_element):
    '''
    Function to convert an xml tree element to python dictionary
    :param tree_element: lxml.etree._Element, an XML element to convert to dicitonary.
    :return: Equivalent python dictionary from the XML.
    '''
    _dict = {tree_element.tag: {} if tree_element.attrib else None}
    children = list(tree_element)
    if children:
        dd = defaultdict(list)
        for dc in map(xml_element_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        _dict = {tree_element.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if tree_element.attrib:
        _dict[tree_element.tag].update(('@' + k, v)
                        for k, v in tree_element.attrib.items())
    if tree_element.text:
        text = tree_element.text.strip()
        if children or tree_element.attrib:
            if text:
              _dict[tree_element.tag]['#text'] = text
        else:
            _dict[tree_element.tag] = text
    return _dict

def get_rpc_example():
    # prepare device infomation
    device_address = "10.96.10.31"
    username = "juniper"
    password = "juniper@123"
    port = 22
    name_aps = []
    # open a connection with the device and start a NETCONF session
    device = Device(host = device_address,
                        user = username,
                        passwd = password,
                        port = port)
    if not device:
        return result
    
    device.open(auto_probe=2)
    device.timeout = 60
    interface_aps = device.rpc.get_aps_information()
    # interface_aps = device.rpc.get_interface_optics_diagnostics_information()

    #Example 1: Use xml_element_to_dict
    result = xml_element_to_dict(interface_aps)
    
    #Example 2: 
    interf_result = interface_aps.xpath('//aps-interface/aps-interface-name')
    if interf_result:
        for interf in interf_result:
            name_aps.append(str(interf.xpath("normalize-space(.)")))
    print(name_aps)

get_rpc_example()