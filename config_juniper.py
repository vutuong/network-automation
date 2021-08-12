#!/usr/bin/env python

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config
import pprint
import sys
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

def get_facts(dev):
    """
    This function get the facts from a juniper device
    :param dev: a connection with the device and start a NETCONF session using from jnpr.junos import Device
    :return: dev.facts
    """
    try:
        dev.open()
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        sys.exit(1)
    print(dev.facts)
    facts = dev.facts
    dev.close()
    return facts

def load_config(dev, conf_file=None, command=None):
    """
    This function loads the config from config_file or a give command to juniper device
    :param dev: a connection with the device and start a NETCONF session using from jnpr.junos import Device
    :param conf_file: the configuration file written in json format 
    :param command: the config command 
    :return: None
    """
    try:
        dev.open()
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        sys.exit(1)

    dev.bind(cu=Config)

    print("### Loading Config from the file: 'configs/vpn1.conf'")
    # Lock the configuration, load configuration changes, and commit
    print ("Locking the configuration")
    try:
        dev.cu.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))
        dev.close()
        return

    print ("Loading configuration changes")
    try:
        if command != None:
            dev.cu.load(command, merge=True)
        else:
            dev.cu.load(path=conf_file, merge=True)
    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))
        print ("Unlocking the configuration")
        try:
                dev.cu.unlock()
        except UnlockError:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print ("Committing the configuration")
    try:
        dev.cu.commit(comment='Loaded by example.')
    except CommitError as err:
        print ("Unable to commit configuration: {0}".format(err))
        print ("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()

    print ("Unlocking the configuration")
    try:
        dev.cu.unlock()
    except UnlockError as err:
        print ("Unable to unlock configuration: {0}".format(err))

    # End the NETCONF session and close the connection
    dev.close()
    return

def main():
    # prepare device infomation
    device_address = "192.168.10.1"
    username = "admin"
    password = "password"
    port = 22

    # open a connection with the device and start a NETCONF session
    dev = Device(host = device_address,
                        user = username,
                        passwd = password,
                        port = port)
    #get facts from device
    get_facts(dev)

    #load and merge config from a file
    conf_file = "configs/op-script.conf"
    load_config(dev, conf_file=conf_file)

    #Exapmle of delete command
    command = "delete system scripts op file test.py"
    load_config(dev, conf_file=None, command=command)

if __name__ == "__main__":
    main()