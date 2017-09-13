# selftest.py
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
from modules.common import SelfTestCommon

class SelfTestBase(object):

    def __init__(self, svrtype, svrcfg, mtm, logger ):
        self.svrtype = svrtype
        self.svrcfg = svrcfg        
        self.mtm = mtm
        self.logger = logger
        self.stc = SelfTestCommon(self.svrtype,self.svrcfg,self.mtm,self.logger)
        self.cfg = self.load_cfg()

        #print ("name = %s"% (__name__, ))

    def testNetworkInterfaceCount(self,system):
        return self.stc.testNetworkInterfaceCount(system)

    def testNetworkLinkStatus(self,system):
        return self.stc.testNetworkLinkStatus(system)

    def testNetworkExternalHost(self, system):
        self.logger.info('testNetworkExternalHosts')        
        return 0

    def testNetwork(self, system):
        self.logger.info('testNetwork')        
        return 0

    def testMemoryCount(self,system):
        self.logger.info('testMemoryCount')        
        return 0

    def testCpu(self,system):
        self.logger.info('testCpu')        
        return 0

    def testStorage(self,system):
        self.logger.info('testStorage')        
        return 0

    ###################################################################
    #
    # Run a command that already produces JSON 
    #
    ###################################################################

    def load_cfg(self):
        return self.stc.load_cfg()

    def run_cmd_jobj(self, cmd):
        return self.stc.run_cmd_jobj(cmd)

    def run_cmd_shell(self, cmd):
        return self.stc.run_cmd_shell(cmd)

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
        return self.stc.payload_kv_pair_convert(payload_str, delimeter)

    def __str__(self):
        return "svrcfg type is %s" % (self.svrcfg)

