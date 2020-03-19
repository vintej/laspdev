#!/usr/bin/python

import pexpect
import time
from lasp_main import set_false, set_true, get_update


def setup_table(laspA, ipA, update, logger_1):
    def exec_cmd(child, cmd, pmt, node):
        child.sendline(cmd)
        child.expect("("+node+"@"+pmt+")")
    def exec_cmd_a(cmda):
        exec_cmd(laspA, cmda, ipA, 'a')

    exec_cmd_a("f().")
    exec_cmd_a('Key1 = <<"key1">>.')
    exec_cmd_a('Key2 = <<"key2">>.')
    exec_cmd_a('Timestamp = fun () -> erlang:unique_integer([monotonic, positive]) end.')
    exec_cmd_a('AwMapType = {state_awmap, [state_mvregister]}.')
    exec_cmd_a('AwMapVarName = <<"awmap">>.')
    exec_cmd_a('AwMapVal = #{what => i_am_111111111110000000000000101111111111101111111111010111111011111111}.')
    exec_cmd_a('AwMapVal2 = #{what => i_am_1000000000010000001010000000011111111111010100000000000100000000011}.')
    exec_cmd_a('{ok, {AwMap, _, _, _}} = lasp:declare({AwMapVarName, AwMapType}, AwMapType).')
    exec_cmd_a('{ok, {AwMap1, _, _, _}} = lasp:update(AwMap, {apply, Key1, {set, Timestamp(), AwMapVal}}, self()).')
    time.sleep(5)
    exec_cmd_a('{ok, AwMapRes} = lasp:query(AwMap1).')
    exec_cmd_a('AwMapRes.')
    set_true()
    logger_1.info("Update==True")
    cnt = 0
    while cnt < 5:
        while True==get_update():
            logger_1.info("Waiting for Update=False")
            time.sleep(5)
        if cnt%2 == 0:
            exec_cmd_a('{ok, _} = lasp:update(AwMap, {apply, Key1, {set, nil, AwMapVal2}}, self()).')
            set_true()
            logger_1.info("Updated and set to true")
        else:
            exec_cmd_a('{ok, _} = lasp:update(AwMap, {apply, Key1, {set, nil, AwMapVal}}, self()).')
            set_true()
            logger_1.info("Updated and set to true")
        logger_1.info("Update==True again")
        time.sleep(10)
        exec_cmd_a('f(AwMapRes1.)')
        exec_cmd_a('{ok, AwMapRes} = lasp:query(AwMap1).')
        exec_cmd_a('AwMapRes1.')
        cnt = cnt+1
    