import os
import time
import sys


def wait_for(this):
    with open('/home/ubuntu/laspdev/containernet_log') as f:
        if this in f.read():
            return True
        else:
            return False

def clean_log():
    os.system("echo '' > /home/ubuntu/laspdev/containernet_log")

def start_bringup():
        clean_log()
        deltaRecv = False
        os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
        time.sleep(5)
        os.system('screen -S containernet -p mininet -X stuff "python3 build_topo.py^M"')
        while deltaRecv == False:
            print('Containernet Getting Ready')
            if wait_for('containernet>'):
                    print("Containernet is Ready")
                    deltaRecv = True
                    break
            time.sleep(10)
        time.sleep(10)
        os.system('screen -S mainTest -p bash -X stuff "python system_main.py start^M"')
        print ('Auto Testing (system_main.py) Starting...')

def stop_bringup():
        clean_log()
        os.system("bash /home/ubuntu/laspdev/kill_lasp.sh")
        print("Killed setup_lasp and system_main")
        time.sleep(2)
        os.system('screen -S containernet -p mininet -X stuff "exit^M"')
        deltaRecv = False
        print("Sent exit to containernet")
        while deltaRecv == False:
            print("Containernet Exiting")
            if wait_for('root@csst-06:/home/ubuntu/laspdev#'):
                    print("Containernet Stopped")
                    deltaRecv = True
                    break
            time.sleep(5)
        time.sleep(5)
        os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
        print("mn --clean")
        clean_log()
        while wait_for('root@csst-06:/home/ubuntu/laspdev#') == False:
            print("Cleaning")
            time.sleep(5)
            'screen -S containernet -p mininet -X stuff "^M"'
            if wait_for('root@csst-06:/home/ubuntu/laspdev#'):
                break
        os.system('screen -S containernet -p mininet -X stuff "service docker restart^M"')
        print("Restarting Docker")
        time.sleep(2)
        print("Stopped")

if len(sys.argv) > 1:
    if sys.argv[1] == "start":
        start_bringup()
    elif sys.argv[1] == "stop":
        stop_bringup()



