#!/usr/bin/python

import pexpect
import time
from lasp_main import set_false, set_true, get_update

def check_update(laspB, ipB, update, logger_2):
    def exec_cmd(child, cmd, pmt, node):
        child.sendline(cmd)
        child.expect("("+node+"@"+pmt+")")
    def exec_cmd_b(cmdb):
        exec_cmd(laspB, cmdb, ipB, 'b')
    cnt = 0
    while cnt<5:
        while False==get_update():
            logger_2.info("Update==False")
            time.sleep(10)
        if cnt != 0:
            exec_cmd_b('f(AwMapRes.)')
        exec_cmd_b('{ok, AwMapRes} = lasp:query({<<"awmap">>,{state_awmap,[state_mvregister]}}).')
        exec_cmd_b("AwMapRes.")
        cnt = cnt+1
        set_false()
        logger_2.info("Query executed, Update==False")
        
    