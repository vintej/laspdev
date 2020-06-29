import os
import time
import sys
import datetime

def wait_for(this):
    with open('/home/ubuntu/Vin/laspdev/containernet_log') as f:
        lineList = f.readlines()
        if this in lineList[len(lineList)-1]:
            return True
        else:
            return False

def clean_log():
    os.system("echo '' > /home/ubuntu/Vin/laspdev/containernet_log")

def start_bringup(jobId, imgC):
        clean_log()
        deltaRecv = False
        os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
        time.sleep(5)
        os.system('screen -S containernet -p mininet -X stuff "python3 overlay.py '+imgC+'^M"')
        while deltaRecv == False:
            print('Containernet Getting Ready')
            if wait_for('containernet>'):
                    print("Containernet is Ready")
                    deltaRecv = True
                    break
            time.sleep(10)
        time.sleep(10)
        os.system('screen -S mainTest -p bash -X stuff "python job4overlay.py '+jobId+'^M"')
        print ('Auto Testing (job4overlay.py) Starting...')

def stop_bringup():
        #clean_log()
        os.system("bash /home/ubuntu/Vin/laspdev/kill_lasp.sh")
        print("Killed setup_lasp, job4overlay and system_main")
        time.sleep(2)
        os.system("echo '' > /home/ubuntu/Vin/laspdev/mainTest_log")
        time.sleep(2)
        if wait_for('containernet>'):
            clean_log()
            os.system('screen -S containernet -p mininet -X stuff "exit^M"')
            deltaRecv = False
            print("Sent exit to containernet")
            while deltaRecv == False:
                print("Containernet Exiting")
                if wait_for('root@csst-11:/home/ubuntu/Vin/laspdev#'):
                    print("Containernet Stopped")
                    deltaRecv = True
                    break
                time.sleep(5)
        time.sleep(5)
        os.system('screen -S containernet -p mininet -X stuff "mn --clean^M"')
        print("mn --clean")
        clean_log()
        while wait_for('root@csst-11:/home/ubuntu/Vin/laspdev#') == False:
            print("Cleaning")
            time.sleep(5)
            'screen -S containernet -p mininet -X stuff "^M"'
            if wait_for('root@csst-11:/home/ubuntu/Vin/laspdev#'):
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
        i = 11
        jIndex = 11
        while i < 21:
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
                with open('/home/ubuntu/Vin/laspdev/mainTest_log') as f:
                    temp = f.read()
                    if ("JOB "+jobId+" FINISHED") in temp:
                        print("Test execution completed ")
                        job_status=True
                        break
                time.sleep(10)
            os.system("cp /home/ubuntu/Vin/laspdev/*_log /home/ubuntu/Vin/laspdev/results/"+jobId+"/"+image+"/")
            print("************FINISHED JOB "+jobId+" for "+image+" ***************")
            i = i + 1
            time.sleep(5)
    elif sys.argv[1] == "varc1":
        i = 1
        run_count = 1
        jobId = 'Varc1_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        while i < 101:
            if i % 20 == 1:
                run_count = 1
                jobId1 = 'Varc1_'+str(i/10+2) #+'_'+str(run_count)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                os.system("python /home/ubuntu/Vin/laspdev/nodesGen/"+str(i/10+2)+"c1generator.py")
            image = 'dev'
            jobId = jobId1+'_'+str(run_count)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            print (jobId+" | "+image)
            time.sleep(2)
            stop_bringup()
            time.sleep(5)
            start_bringup(jobId, image)
            job_status = False
            while job_status==False:
                with open('/home/ubuntu/Vin/laspdev/mainTest_log') as f:
                    temp = f.read()
                    if ("JOB "+jobId+" FINISHED") in temp:
                        print("Test execution completed ")
                        job_status=True
                        break
                time.sleep(10)
            os.system("cp /home/ubuntu/Vin/laspdev/*_log /home/ubuntu/Vin/laspdev/results/"+jobId+"/"+image+"/")
            print("************FINISHED JOB "+jobId+" for "+image+" ***************")
            i = i + 1
            run_count = run_count + 1
            time.sleep(5)
    elif sys.argv[1] == "varc1Edge":
        i = 1
        run_count = 1
        jobId = 'Varc1Edge_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        c1Edge = 2
        while i < 26:
            if i % 5 == 1:
                run_count = 1
                jobId1 = 'Varc1Edge_'+str(c1Edge) #+'_'+str(run_count)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%$
                os.system("python /home/ubuntu/Vin/laspdev/nodesGen/"+str(i/10+2)+"c1generator.py")
                print("python /home/ubuntu/Vin/laspdev/nodesGen/"+str(c1Edge)+"c1generator.py")
                c1Edge = c1Edge + 2
            image = 'dev'
            jobId = jobId1+'_'+str(run_count)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            print (jobId+" | "+image)
            time.sleep(2)
            stop_bringup()
            time.sleep(5)
            start_bringup(jobId, image)
            job_status = False
            while job_status==False:
                with open('/home/ubuntu/Vin/laspdev/mainTest_log') as f:
                    temp = f.read()
                    if ("JOB "+jobId+" FINISHED") in temp:
                        print("Test execution completed ")
                        job_status=True
                        break
                time.sleep(10)
            os.system("cp /home/ubuntu/Vin/laspdev/*_log /home/ubuntu/Vin/laspdev/results/"+jobId+"/"+image+"/")
            print("************FINISHED JOB "+jobId+" for "+image+" ***************")
            i = i + 1
            run_count = run_count + 1
            time.sleep(5)
    if sys.argv[1] != "stop":
        job_status = False
        while job_status==False:
            with open('/home/ubuntu/Vin/laspdev/mainTest_log') as f:
                temp = f.read()
                if ("JOB "+jobId+" FINISHED") in temp:
                    print("Test execution completed")
                    job_status=True
                    break

else:
    i = 1
    jIndex = 1
    changec1 = 7000
    while i < 41:
        if i % 2 == 1:
            jobId = 'OverlayTest_c1_7_'+str(changec1)+'_valTime_6_30min_'+str(jIndex)+'_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            image = 'base'
        else:
            #if jIndex != 1:
            #os.system("sed -i 's+RATE_C1="+str(changec1)+"+RATE_C1="+str(changec1+1000)+"+g' /home/ubuntu/Vin/laspdev/utility/setup_lasp.py")
            #changec1 = changec1 + 1000
            image = 'dev'
            jIndex = jIndex + 1 
        time.sleep(0.5)
        print (jobId+" | "+image)
        time.sleep(2)
        stop_bringup()
        time.sleep(2)
        start_bringup(jobId, image)
        job_status = False
        cTempX = 1
        while job_status==False:
            if cTempX % 120 == 1:
                print(jobId+" | "+image+" is running")
            with open('/home/ubuntu/Vin/laspdev/mainTest_log') as f:
                temp = f.read()
                if ("JOB "+jobId+" FINISHED") in temp:
                    print("Test execution completed")
                    job_status=True
                    break
            cTempX = cTempX + 1
            time.sleep(5)
        os.system("cp /home/ubuntu/Vin/laspdev/*_log /home/ubuntu/Vin/laspdev/results/"+jobId+"/"+image+"/")
        print("************FINISHED JOB "+jobId+" for "+image+" ***************")
        i = i + 1
        time.sleep(5)

