#########################################################################
# Python program that can do the following in the Kali VM:
#   1. Enumerate all the running processes.
#   2. List all the running threads within process boundary.
#   3. Enumerate all the loaded modules within the processes.
#   4. Is able to show all the executable pages within the processes.
#   5. Gives us a capability to read the memory.
#-----------------------------------------------------------------------
import os
import threading
import psutil

def print_processes():

    # Get pids from processes in /proc
    #pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    #print("Got pids from /proc")
    
    print("\nProcesses:")
    count = 0
    
    # Loop over /proc and print all Process Data
    for proc in psutil.process_iter():
        try:
            count += 1
            process_name = proc.name()
            pid = proc.pid
            current_processes.append(pid)
            print(str(count) + ". ", pid, ':', process_name)

        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
#    for pid in pids:
#        try:
#            process_name = open('/proc/%s/cmdline' % pid, 'rb').read()
#            if process_name:
#                count += 1
#                print(str(count) + ". PID: " + pid + "\t" + process_name)
#                current_processes.append(pid)
#        except:
#            pass
#    return current_processes
    
def print_threads():
    print("\nThreads:")
    for thread in threading.enumerate():
        print(thread.name)

def print_modules(pid):
    # Print loaded modules
    #for pid in current_processes:
        try:
            p = psutil.Process(pid)
            print("\nProcess", pid, "modules:")
            for mod in p.memory_maps():
                print(mod.path)
        
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
   
def print_executables(pid):
    #print("\nExecutables in processes:")
    #for pid in current_processes:
        #print("\n", pid, ":")
        #proc_path = '/proc/' + str(pid)
        #for file in os.listdir(proc_path):
            #if os.access(proc_path, os.X_OK):
                #print(file)
    print("\nExecutables in process", pid, ":")
    proc_path = '/proc/' + str(pid)
    for file in os.listdir(proc_path):
        if os.access(proc_path, os.X_OK):
            print(file)

if __name__=='__main__':
    current_processes = []
    print_processes()
    print_threads()
    
    print("\nWhich process would you like to see loaded modules and executables for?: (Process ID)")
    user_pid = input()
    print_modules(int(user_pid))
    print_executables(int(user_pid))
