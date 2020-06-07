import os
import time

os.system("echo '' > /home/ubuntu/laspdev/containernet_log")
deltaRecv = False
os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
time.sleep(5)
os.system('screen -S containernet -p mininet -X stuff "python3 build_topo.py^M"')
while deltaRecv == False:
        print('Test')
        with open('/home/ubuntu/laspdev/containernet_log') as f:
                if 'containernet>' in f.read():
                    print("Coming here")
                    deltaRecv = True
                    break
        time.sleep(10)
time.sleep(10)
os.system('screen -S mainTest -p bash -X stuff "python system_main.py^M"')
print ('Finished')
