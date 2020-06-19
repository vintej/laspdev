import os
import time
import sys
import datetime

def wait_for(this):
    with open('/home/ubuntu/laspdev/containernet_log') as f:
        lineList = f.readlines()
        if this in lineList[len(lineList)-1]:
            return True
        else:
            return False

def clean_log():
    os.system("echo '' > /home/ubuntu/laspdev/containernet_log")

def start_bringup(jobId, imgC):
        clean_log()
        deltaRecv = False
        os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
        time.sleep(5)
        os.system('screen -S containernet -p mininet -X stuff "python3 build_topo.py '+imgC+'^M"')
        while deltaRecv == False:
            print('Containernet Getting Ready')
            if wait_for('containernet>'):
                    print("Containernet is Ready")
                    deltaRecv = True
                    break
            time.sleep(10)
        time.sleep(10)
        os.system('screen -S mainTest -p bash -X stuff "python system_main.py '+jobId+'^M"')
        print ('Auto Testing (system_main.py) Starting...')

def stop_bringup():
        #clean_log()
        os.system("bash /home/ubuntu/laspdev/kill_lasp.sh")
        print("Killed setup_lasp and system_main")
        time.sleep(2)
        os.system("echo '' > /home/ubuntu/laspdev/mainTest_log")
        time.sleep(2)
        if wait_for('containernet>'):
            clean_log()
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
    jobId = 'NewRunTest'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    #jobId = 'deltaTest'
    if sys.argv[1] == "start":
        stop_bringup()
        jobId = "start"
        start_bringup(jobId, 'dev')
    elif sys.argv[1] == 'deltaTest':
        jobId = 'deltaTest'
        stop_bringup()
        start_bringup(jobId, 'dev')
    elif sys.argv[1] == "stop":
        stop_bringup()
    elif sys.argv[1] == "restart":
        stop_bringup()
        time.sleep(2)
        start_bringup(jobId, 'base')
    elif sys.argv[1] == "regression":
        i = 1
        jIndex = 1
        while i < 11:
            jobId = 'Regression'+str(jIndex)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            image = 'dev'
            jIndex = jIndex + 1
            time.sleep(0.5)
            print (jobId+" | "+image)
            time.sleep(2)
            stop_bringup()
            time.sleep(5)
            start_bringup(jobId, image)
            job_status = False
            while job_status==False:
                with open('/home/ubuntu/laspdev/mainTest_log') as f:
                    temp = f.read()
                    if ("JOB "+jobId+" FINISHED") in temp:
                        print("Test execution completed ")
                        job_status=True
                        break
                time.sleep(10)
            os.system("cp /home/ubuntu/laspdev/*_log /home/ubuntu/laspdev/results/"+jobId+"/"+image+"/")
            print("************FINISHED JOB "+jobId+" for "+image+" ***************")
            i = i + 1
            time.sleep(5)
    if sys.argv[1] != "stop":
        job_status = False
        while job_status==False:
            with open('/home/ubuntu/laspdev/mainTest_log') as f:
                temp = f.read()
                if ("JOB "+jobId+" FINISHED") in temp:
                    print("Test execution completed")
                    job_status=True
                    break

else:
    i = 1
    jIndex = 1
    while i < 201:
        if i % 2 == 1:
            jobId = 'AutoTest'+str(jIndex)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            image = 'base'
        else:
            image = 'dev'
            jIndex = jIndex + 1 
        time.sleep(0.5)
        print (jobId+" | "+image)
        time.sleep(2)
        stop_bringup()
        time.sleep(2)
        start_bringup(jobId, image)
        job_status = False
        while job_status==False:
            with open('/home/ubuntu/laspdev/mainTest_log') as f:
                temp = f.read()
                if ("JOB "+jobId+" FINISHED") in temp:
                    print("Test execution completed")
                    job_status=True
                    break
            time.sleep(5)
        os.system("cp /home/ubuntu/laspdev/*_log /home/ubuntu/laspdev/results/"+jobId+"/"+image+"/")
        print("************FINISHED JOB "+jobId+" for "+image+" ***************")
        i = i + 1
        time.sleep(5)

