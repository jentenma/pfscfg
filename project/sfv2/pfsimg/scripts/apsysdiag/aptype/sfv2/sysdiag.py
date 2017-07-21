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

class SysDiagBase(object):

    def __init__(self, svrcfg, setup_info, logger ):
        self.svrcfg = svrcfg
        self.setup_info = setup_info
        self.logger = logger
        #print ("name = %s"% (__name__, ))
        
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

    def __str__(self):
        return "svrcfg type is %s" % (self.svrcfg)
