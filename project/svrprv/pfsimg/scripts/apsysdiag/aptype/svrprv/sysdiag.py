# sysdiag.py
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

import json
import pprint
import telnetlib
import logging
import os
import errno
import atexit
import subprocess
import socket
import time
import threading

class SysDiagBase(object):

    def __init__(self, svrtype, svrcfg, mtm, logger ):
        self.svrtype = svrtype
        self.svrcfg = svrcfg        
        self.mtm = mtm
        self.logger = logger
        self.cfg = self.load_cfg()
        self.thread_list = []
        
        #print self.cfg['diagconf']
        
        #print ("name = %s"% (__name__, ))

    def testNetworkInterfaceCount(self,system):
        self.logger.info('testNetwork')
        cmd = "/opt/system/pfs_diags/bin/jnetinterfaces"
        # get the interfaces that are present
        jobj = self.run_cmd_jobj(cmd)

        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(jobj)

        # Iterate over the expected values and see if they are in the actual values
        # The actual interfaces may show up in a different order.

        act_ifc = jobj['interfaces']
        exp_ifc = self.cfg['interfaces']
        num_exp = len(exp_ifc.keys())
        num_act = 0;
        for ekey, evalue in exp_ifc.iteritems():
            for akey, avalue in act_ifc.iteritems():
                if (evalue == avalue):
                    self.logger.info("%s found"%evalue)
                    num_act = num_act + 1
                    break
        self.logger.info("expected %d actual %d"%(num_exp,num_act))                
        if (num_act == num_exp):
            return 0
        return 1

    def testNetworkLinkStatus(self,system):
        self.logger.info('testNetworkLinkStatus')
        pp = pprint.PrettyPrinter(indent=4)

        # Iterate over the expected values and see if they are in the actual values
        # The actual interfaces may show up in a different order.

        exp_ifc = self.cfg['interfaces']
        num_exp = len(exp_ifc.keys())

        num_fail = 0
        for ekey, evalue in exp_ifc.iteritems():
            cmd = "/usr/sbin/ethtool "+evalue
            outstr = self.run_cmd_shell(cmd)
            jobj = self.payload_kv_pair_convert(outstr, ': ')
            # pp.pprint(jobj)
            #
            # It will suck if ethtool changes the verbiage but oh well...
            #
            self.logger.info("%s Link detected: %s"%(evalue,jobj['Link detected']))                
            if (jobj['Link detected'] != 'yes'):
                num_fail = num_fail + 1

        if (num_fail):
            return 1

        return 0

    def testNetworkExternalHost(self, system):
        self.logger.info('testNetworkExternalHosts')        
        return 0

    def testNetwork(self, system):
        self.logger.info('testNetwork')        
        return 0

    def testMemory(self,system):
        self.logger.info('testMemory')        
        return 0

    def testCpu(self,system):
        self.logger.info('testCpu')        
        return 0

    def testStorage(self,system):
        self.logger.info('testStorage')        
        return 0

    def testFabricPing(self,system):
        self.logger.info('testFabricPing')                

        hostname = socket.gethostname()
        hostlist = self.cfg['diagconf']['nodelist']
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(hostlist)

        status = 0
        for host in hostlist.split():
            if (host == hostname):
                continue
            fabhost = host+"-fab"
            if self.ping_chk(fabhost, 1):
                self.logger.info("%s is alive"%fabhost)
            else:
                status = 1
                self.logger.error("%s is NOT alive"%fabhost)                

        return status

    def testFabricIPerf3(self,system):
        self.logger.info('testFabricIperf3')                

        cmd = "/opt/system/pfs_diags/bin/jnetinterfaces"
        # get the interfaces that are present
        jobj = self.run_cmd_jobj(cmd)

        hostname = socket.gethostname()

        hostlist = self.cfg['diagconf']['nodelist']

        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(hostlist)

        # Run a ping check to make sure everybody is reachable
        status = self.testFabricPing(system)
        if (status):
            self.logger.error("Ping check failed prior to iperf3 being run")
            return 1

        
        #
        # First things first. Start up an iperf3 server
        #
        cmd = "/usr/bin/iperf3 -s -D"
        outstr = self.run_cmd_shell(cmd)
        if (outstr == None):
            self.logger.error("iperf3 listener daemon failed to start")
            return 1


        for host in hostlist.split():
            if (host == hostname):
                continue

            fabhost = host+"-fab"

            cmd = "/usr/bin/iperf3 -c "+fabhost+" -i 1 -t 30"
            t = threading.Thread(target=self.run_cmd_shell, name="iperf3",args=(cmd))
            t.start()

            self.thread_list.append(t)
            
        for t in self.thread_list:
            t.join()
            
        return 0

        # Iterate over the expected values and see if they are in the actual values
        # The actual interfaces may show up in a different order.

        act_ifc = jobj['interfaces']
        exp_ifc = self.cfg['interfaces']
        num_exp = len(exp_ifc.keys())
        num_act = 0;
        for ekey, evalue in exp_ifc.iteritems():
            for akey, avalue in act_ifc.iteritems():
                if (evalue == avalue):
                    self.logger.info("%s found"%evalue)
                    num_act = num_act + 1
                    break
        self.logger.info("expected %d actual %d"%(num_exp,num_act))                
        if (num_act == num_exp):
            return 0
        return 1
        
        self.logger.info('testFabricIperf3')        
        return 0


    ###################################################################
    #
    # Ping check 
    #
    ###################################################################

    def ping_chk(self, host, tries):
        pause_between_pings = 0
        pings = 0
        cmd = 'ping'
        while pings < tries:
            reply = subprocess.call(['%s' % cmd, '-q', '-c1', '-W1', '%s' % host], \
                                    stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
                                    # sys util rc == 0 means success so invert
            reply = not reply
            if reply:
                return True
            else:
                pings += 1
                time.sleep(pause_between_pings)

            return False
                
    ###################################################################
    #
    # Load the configuration for the system.
    #
    ###################################################################


    def load_cfg(self):
        svrtype = self.svrtype
        svrcfg = self.svrcfg
        logger = self.logger
        filename = "/opt/system/pfs/scripts/apsysdiag/cfg/cfg-"+svrtype+"-"+svrcfg+".json"
        logger.info("config file: %s"%filename)
        cfg_info = json.load(open(filename))
        cmd = "cat /etc/pfs.d/diag.conf "
        outstr = self.run_cmd_shell(cmd)
        jobj = self.payload_kv_pair_convert(outstr, ': ')
        cfg_info['diagconf'] = jobj
        return cfg_info

    ###################################################################
    #
    # Run a command that already outputs JSON
    #
    ###################################################################

    def run_cmd_jobj(self, cmd):
        logger = self.logger
        logger.info("command: %s"%cmd)
        
        try:
            output = subprocess.check_output(cmd,stdin=None,stderr=None,shell=True,universal_newlines=False)
        except subprocess.CalledProcessError as e:
            output = "?Command "+cmd+" Failed?"
            errmsg = {"description": output}
            return None
        except OSError:
            output = "?Command "+cmd+" Not Found?"
            errmsg = {"description": output}
            return None

        # Inventory Commands already produces a JSON string. Convert to a dictionary
        # so the reply can parse it.
        jobj = json.loads(output)
        return jobj

    def run_cmd_shell(self, cmd):
        logger = self.logger
        logger.info("command: %s"%cmd)
        
        try:
            output = subprocess.check_output(cmd,stdin=None,stderr=None,shell=True,universal_newlines=False)
        except subprocess.CalledProcessError as e:
            output = "?Command "+cmd+" Failed?"
            errmsg = {"description": output}
            return None
        except OSError:
            output = "?Command "+cmd+" Not Found?"
            errmsg = {"description": output}
            return None

        return output


    #
    # The assumption here is that the output of the shell command
    # is already in a key value pair. The key value pair must be seperated
    # by a character sequence. In all cases tested so for the sequence is ": "
    #
    # If a line is hit that doesn't result in a key value pair the last key
    # will be used with a number sequence prepended to it.
    # This take care if the case where values for a given key are in multiple
    # lines
    #
    def payload_kv_pair_convert(self, payload_str, delimeter):
        plist = payload_str.splitlines()
        pkey_dict = dict()
        key = "na"
        no_key_num = 1
        for kv in plist:
            tokens = kv.split(delimeter)
            if len(tokens) != 2:
                key = str(no_key_num)+"-"+key
                no_key_num = no_key_num + 1
                v = kv.strip()
            else:
                k,v = kv.split(delimeter)
                key = k.strip()

            value = v.rstrip()
            pkey_dict[key] = value

        return pkey_dict

    def __str__(self):
        return "svrcfg type is %s" % (self.svrcfg)

