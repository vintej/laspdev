#!/usr/bin/python

import pexpect
import time

update = False

def get_update():
    global update
    return update

def set_false():
    global update
    update = False

def set_true():
    global update
    update = True

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
    exec_cmd_a("AwMapRes.")
    set_true()
    logger_1.info("Update==True")
    cnt = 1
    update_cnt = 0
    while cnt <= 9:
        while True==get_update():
            logger_1.info("Waiting for Update=False")
            time.sleep(5)
        if cnt%2 == 0:
            exec_cmd_a('{ok, _} = lasp:update(AwMap, {apply, Key1, {set, nil, AwMapVal2}}, self()).')
            set_true()
            update_cnt = update_cnt + 1
            logger_1.info("Update Count: "+str(update_cnt))
        else:
            exec_cmd_a('{ok, _} = lasp:update(AwMap, {apply, Key1, {set, nil, AwMapVal}}, self()).')
            set_true()
            update_cnt = update_cnt + 1
            logger_1.info("Update Count: "+str(update_cnt))
        logger_1.info("Update==True again & loop count: "+str(cnt))
        time.sleep(10)
        exec_cmd_a('f(AwMapRes).')
        exec_cmd_a('{ok, AwMapRes} = lasp:query(AwMap1).')
        exec_cmd_a('AwMapRes.')
        cnt = cnt+1

def check_update(laspB, ipB, update, logger_2):
    def exec_cmd(child, cmd, pmt, node):
        child.sendline(cmd)
        child.expect("("+node+"@"+pmt+")")
    def exec_cmd_b(cmdb):
        exec_cmd(laspB, cmdb, ipB, 'b')
    cntb = 1
    exp1 = True
    read_cnt = 0
    while cntb<=9:
        while False==get_update():
            logger_2.info("Update==False")
            time.sleep(10)
        #if cntb != 0:
        time.sleep(10)
        #    logger_2.info("F() for AwMapRes.")
        if cntb%3==0:
            #time.sleep(10)
            exec_cmd_b('{ok, AwMapRes} = lasp:query({<<"awmap">>,{state_awmap,[state_mvregister]}}).')
            exec_cmd_b("AwMapRes.")
            read_cnt = read_cnt + 1
            logger_2.info("Read Count: "+str(read_cnt))
            x = str(laspB.before.splitlines())
            logger_2.info("Before: "+x)
            #logger_2.info("After: "+str(laspB.after.splitlines()))
            if 'i_am_111111111110000000000000101111111111101111111111010111111011111111' in x: #and exp1==True:
                set_false()
                exp1 = False
                logger_2.info("Read 11 and exp1 set to False, expecting 10 in next")
            if 'i_am_1000000000010000001010000000011111111111010100000000000100000000011' in x: #and exp1==False:
                set_false()
                exp1 = True
                logger_2.info("Read 10 and exp1 set to True, expecting 11 in next")
            logger_2.info("Query executed loop Count:"+str(cntb))
            exec_cmd_b('f(AwMapRes).')
            cntb = cntb+1
        elif cntb==9:
            logger_2.info("Last Loop: "+str(cntb))
            set_false()
            cntb = cntb + 1
        else:
            cntb = cntb+1
            logger_2.info("No READ and loop Count: "+str(cntb))
            set_false()
            time.sleep(30)