# saba.py
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
import errno
import atexit
import subprocess
import re
import selftest
import modules.common

class SelfTest(selftest.SelfTestBase):
        
    def __str__(self):
        return "Server Config is %s" % (self.svrcfg,)


    #
    # For memory information we need to use ipmitool
    #

    # Saba 
    # Product Manufacturer  : ad80
    # Product Name          : 0b
    # Product Part Number   : HMT41GR7BFR8A-PB
    # Product Version       : 3454
    # Product Serial        : 3132b01a
     
                
    def testMemoryCount(self,system):
        self.logger.info('testMemoryCount')
        pp = pprint.PrettyPrinter(indent=4)        

        return self.stc.testMemoryCountDeviceTree(system)
    
